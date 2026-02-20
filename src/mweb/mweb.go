package main

//#include <stdlib.h>
import "C"

import (
	"encoding/json"
	"strings"
	"unsafe"

	"github.com/ltcmweb/ltcd/chaincfg"
	"github.com/ltcmweb/ltcd/ltcutil/psbt"
	"github.com/ltcmweb/mwebd/sign"
)

func doReq[Req, Resp any](s *C.char, f func(*Req) (Resp, error)) *C.char {
	var req Req
	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}
	resp, err := f(&req)
	if err != nil {
		return C.CString(err.Error())
	}
	b, _ := json.Marshal(resp)
	return C.CString(string(b))
}

//export Addresses
func Addresses(s *C.char) *C.char {
	return doReq(s, func(req *sign.AddressesRequest) (sign.AddressesResponse, error) {
		return sign.Addresses(req, &chaincfg.MainNetParams), nil
	})
}

//export AddressesPubKeyHash
func AddressesPubKeyHash(s *C.char) *C.char {
	return doReq(s, func(req *sign.AddressesPubKeyHashRequest) (sign.AddressesResponse, error) {
		return sign.AddressesPubKeyHash(req, &chaincfg.MainNetParams)
	})
}

//export PsbtGetRecipients
func PsbtGetRecipients(s *C.char) *C.char {
	return doReq(s, func(req *sign.Psbt) (sign.PsbtGetRecipientsResponse, error) {
		return sign.PsbtGetRecipients(req, &chaincfg.MainNetParams)
	})
}

//export PsbtSign
func PsbtSign(s *C.char) *C.char {
	return doReq(s, sign.PsbtSign)
}

//export PsbtSignPubKeyHash
func PsbtSignPubKeyHash(s *C.char) *C.char {
	return doReq(s, sign.PsbtSignPubKeyHash)
}

//export PsbtFinalize
func PsbtFinalize(s *C.char) *C.char {
	return doReq(s, func(req *sign.Psbt) (resp sign.Psbt, err error) {
		p, err := psbt.NewFromRawBytes(strings.NewReader(req.PsbtB64), true)
		if err != nil {
			return
		}
		if err = psbt.MaybeFinalizeAll(p); err != nil {
			return
		}
		resp.PsbtB64, err = p.B64Encode()
		return
	})
}

//export FreeCString
func FreeCString(s *C.char) {
	C.free(unsafe.Pointer(s))
}

func main() {}
