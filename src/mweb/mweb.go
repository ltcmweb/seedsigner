package main

//#include <stdlib.h>
import "C"

import (
	"encoding/hex"
	"encoding/json"
	"errors"
	"strings"
	"unsafe"

	"github.com/ltcmweb/ltcd/btcec/v2"
	"github.com/ltcmweb/ltcd/chaincfg"
	"github.com/ltcmweb/ltcd/ltcutil"
	"github.com/ltcmweb/ltcd/ltcutil/mweb"
	"github.com/ltcmweb/ltcd/ltcutil/mweb/mw"
	"github.com/ltcmweb/ltcd/ltcutil/psbt"
	"github.com/ltcmweb/ltcd/txscript"
	"github.com/ltcmweb/ltcd/wire"
)

var cp = chaincfg.MainNetParams

//export Addresses
func Addresses(s *C.char) *C.char {
	var req struct {
		ScanSecret  []byte `json:""`
		SpendPubkey []byte `json:""`
		FromIndex   uint32 `json:""`
		ToIndex     uint32 `json:""`
	}
	var resp struct {
		Address []string `json:""`
	}

	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}

	keychain := &mweb.Keychain{
		Scan:        (*mw.SecretKey)(req.ScanSecret),
		SpendPubKey: (*mw.PublicKey)(req.SpendPubkey),
	}

	for i := req.FromIndex; i < req.ToIndex; i++ {
		addr := ltcutil.NewAddressMweb(keychain.Address(i), &cp)
		resp.Address = append(resp.Address, addr.String())
	}

	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export PsbtGetRecipients
func PsbtGetRecipients(s *C.char) *C.char {
	type PsbtRecipient struct {
		Address string `json:""`
		Value   int64  `json:""`
	}
	var req struct {
		PsbtB64 string `json:""`
	}
	var resp struct {
		Recipient    []*PsbtRecipient `json:""`
		InputAddress []string         `json:""`
		Fee          int64            `json:""`
	}

	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}

	p, err := psbt.NewFromRawBytes(strings.NewReader(req.PsbtB64), true)
	if err != nil {
		return C.CString(err.Error())
	}

	pkScriptToAddr := func(pkScript []byte) (string, error) {
		_, addrs, _, err := txscript.ExtractPkScriptAddrs(pkScript, &cp)
		if err != nil {
			return "", err
		}
		var addrs2 []string
		for _, addr := range addrs {
			addrs2 = append(addrs2, addr.String())
		}
		return strings.Join(addrs2, ","), nil
	}

	for _, pInput := range p.Inputs {
		var addr string
		switch {
		case pInput.WitnessUtxo != nil:
			addr, _ = pkScriptToAddr(pInput.WitnessUtxo.PkScript)
			resp.Fee += pInput.WitnessUtxo.Value
		case pInput.MwebOutputId != nil:
			addr = hex.EncodeToString(pInput.MwebOutputId[:])
		}
		resp.InputAddress = append(resp.InputAddress, addr)
	}

	for _, pOutput := range p.Outputs {
		var addr string
		switch {
		case pOutput.StealthAddress != nil:
			addr = ltcutil.NewAddressMweb(pOutput.StealthAddress, &cp).String()
		case pOutput.OutputCommit != nil:
			addr = cp.Bech32HRPMweb + "1"
		default:
			if addr, err = pkScriptToAddr(pOutput.PKScript); err != nil {
				return C.CString(err.Error())
			}
			resp.Fee -= int64(pOutput.Amount)
		}
		resp.Recipient = append(resp.Recipient, &PsbtRecipient{
			Address: addr,
			Value:   int64(pOutput.Amount),
		})
	}

	for _, pKernel := range p.Kernels {
		for _, pegout := range pKernel.PegOuts {
			addr, err := pkScriptToAddr(pegout.PkScript)
			if err != nil {
				return C.CString(err.Error())
			}
			resp.Recipient = append(resp.Recipient, &PsbtRecipient{
				Address: addr,
				Value:   pegout.Value,
			})
		}
		if pKernel.Fee != nil {
			resp.Fee += int64(*pKernel.Fee)
		}
		if pKernel.PeginAmount != nil {
			resp.Fee -= int64(*pKernel.PeginAmount)
		}
	}

	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export PsbtSign
func PsbtSign(s *C.char) *C.char {
	var req struct {
		PsbtB64     string `json:""`
		ScanSecret  []byte `json:""`
		SpendSecret []byte `json:""`
	}
	var resp struct {
		PsbtB64 string `json:""`
	}

	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}

	p, err := psbt.NewFromRawBytes(strings.NewReader(req.PsbtB64), true)
	if err != nil {
		return C.CString(err.Error())
	}

	keychain := &mweb.Keychain{
		Scan:  (*mw.SecretKey)(req.ScanSecret),
		Spend: (*mw.SecretKey)(req.SpendSecret),
	}

	addrIndex := map[mw.PublicKey]uint32{}
	for _, pInput := range p.Inputs {
		if pInput.MwebOutputPubkey != nil && pInput.MwebAddressIndex != nil {
			addrIndex[*pInput.MwebOutputPubkey] = *pInput.MwebAddressIndex
		}
	}

	inputSigner := psbt.BasicMwebInputSigner{DeriveOutputKeys: func(
		Ko, Ke *mw.PublicKey, t *mw.SecretKey) (
		*mw.BlindingFactor, *mw.SecretKey, error) {

		if t == nil {
			sA := Ke.Mul(keychain.Scan)
			t = (*mw.SecretKey)(mw.Hashed(mw.HashTagDerive, sA[:]))
		}

		htOutKey := (*mw.SecretKey)(mw.Hashed(mw.HashTagOutKey, t[:]))
		B_i := Ko.Div(htOutKey)
		addr := &mw.StealthAddress{Scan: B_i.Mul(keychain.Scan), Spend: B_i}
		if !addr.Equal(keychain.Address(addrIndex[*Ko])) {
			return nil, nil, errors.New("address mismatch")
		}

		return (*mw.BlindingFactor)(mw.Hashed(mw.HashTagBlind, t[:])),
			keychain.SpendKey(addrIndex[*Ko]).Mul(htOutKey), nil
	}}

	signer, err := psbt.NewSigner(p, inputSigner)
	if err != nil {
		return C.CString(err.Error())
	}

	if _, err = signer.SignMwebComponents(); err != nil {
		return C.CString(err.Error())
	}

	if resp.PsbtB64, err = p.B64Encode(); err != nil {
		return C.CString(err.Error())
	}

	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export PsbtSignNonMweb
func PsbtSignNonMweb(s *C.char) *C.char {
	var req struct {
		PsbtB64 string `json:""`
		PrivKey []byte `json:""`
		Index   uint32 `json:""`
	}
	var resp struct {
		PsbtB64 string `json:""`
	}

	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}

	p, err := psbt.NewFromRawBytes(strings.NewReader(req.PsbtB64), true)
	if err != nil {
		return C.CString(err.Error())
	}

	tx, err := psbt.ExtractUnsignedTx(p)
	if err != nil {
		return C.CString(err.Error())
	}

	txInIdx := 0
	fetcher := txscript.NewMultiPrevOutFetcher(nil)
	for i, pInput := range p.Inputs {
		if pInput.MwebOutputId == nil {
			op := wire.NewOutPoint(pInput.PrevoutHash, *pInput.PrevoutIndex)
			fetcher.AddPrevOut(*op, pInput.WitnessUtxo)
			if i < int(req.Index) {
				txInIdx++
			}
		}
	}

	txOut := p.Inputs[req.Index].WitnessUtxo
	key, pub := btcec.PrivKeyFromBytes(req.PrivKey)
	sig, err := txscript.RawTxInWitnessSignature(tx,
		txscript.NewTxSigHashes(tx, fetcher), txInIdx,
		txOut.Value, txOut.PkScript, txscript.SigHashAll, key)
	if err != nil {
		return C.CString(err.Error())
	}

	u := psbt.Updater{Upsbt: p}
	_, err = u.Sign(int(req.Index), sig, pub.SerializeCompressed(), nil, nil)
	if err != nil {
		return C.CString(err.Error())
	}
	if err = psbt.Finalize(p, int(req.Index)); err != nil {
		return C.CString(err.Error())
	}

	if resp.PsbtB64, err = p.B64Encode(); err != nil {
		return C.CString(err.Error())
	}

	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export FreeCString
func FreeCString(s *C.char) {
	C.free(unsafe.Pointer(s))
}

func main() {}
