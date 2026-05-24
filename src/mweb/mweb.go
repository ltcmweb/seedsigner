package main

//#include <stdlib.h>
import "C"

import (
	"bytes"
	"encoding/binary"
	"errors"
	"unsafe"

	"github.com/ltcmweb/ltcd/chaincfg"
	"github.com/ltcmweb/mwebd/sign"
)

//export mweb
func mweb(fn *C.char, m *byte, mlen C.size_t, cerr **C.char) *byte {
	resp, err := doReq(C.GoString(fn), unsafe.Slice(m, mlen))
	if err != nil {
		*cerr = C.CString(err.Error())
		return nil
	}
	return resp
}

func doReq(fn string, m []byte) (*byte, error) {
	r := bytes.NewReader(m)
	switch fn {
	case "Addresses":
		var req sign.AddressesRequest
		if err := req.Deserialize(r); err != nil {
			return nil, err
		}
		resp := sign.Addresses(&req, &chaincfg.MainNetParams)
		return doResp(&resp)
	case "AddressesPubKeyHash":
		var req sign.AddressesPubKeyHashRequest
		if err := req.Deserialize(r); err != nil {
			return nil, err
		}
		resp, err := sign.AddressesPubKeyHash(&req, &chaincfg.MainNetParams)
		if err != nil {
			return nil, err
		}
		return doResp(&resp)
	case "PsbtGetRecipients":
		var req sign.Psbt
		if err := req.Deserialize(r); err != nil {
			return nil, err
		}
		resp, err := sign.PsbtGetRecipients(&req, &chaincfg.MainNetParams)
		if err != nil {
			return nil, err
		}
		return doResp(&resp)
	case "PsbtSign":
		var req sign.PsbtSignRequest
		if err := req.Deserialize(r); err != nil {
			return nil, err
		}
		resp, err := sign.PsbtSign(&req)
		if err != nil {
			return nil, err
		}
		return doResp(&resp)
	case "PsbtSignPubKeyHash":
		var req sign.PsbtSignPubKeyHashRequest
		if err := req.Deserialize(r); err != nil {
			return nil, err
		}
		resp, err := sign.PsbtSignPubKeyHash(&req)
		if err != nil {
			return nil, err
		}
		return doResp(&resp)
	case "PsbtFinalize":
		var req sign.Psbt
		if err := req.Deserialize(r); err != nil {
			return nil, err
		}
		resp, err := sign.PsbtFinalize(&req)
		if err != nil {
			return nil, err
		}
		return doResp(&resp)
	}
	return nil, errors.New("function unrecognized")
}

func doResp(resp sign.Message) (*byte, error) {
	var cw sign.CountWriter
	if err := resp.Serialize(&cw); err != nil {
		return nil, err
	}
	m := (*byte)(C.malloc(C.size_t(cw.Len + 4)))
	if m == nil {
		return nil, errors.New("malloc failed")
	}
	buf := bytes.NewBuffer(unsafe.Slice(m, cw.Len+4)[:0])
	binary.Write(buf, binary.LittleEndian, uint32(cw.Len))
	if err := resp.Serialize(buf); err != nil {
		C.free(unsafe.Pointer(m))
		return nil, err
	}
	return m, nil
}
