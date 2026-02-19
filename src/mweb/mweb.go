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

var cp = chaincfg.MainNetParams

//export Addresses
func Addresses(s *C.char) *C.char {
	var req sign.AddressesRequest
	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}
	resp := sign.Addresses(&req, &cp)
	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export AddressesPubKeyHash
func AddressesPubKeyHash(s *C.char) *C.char {
	var req sign.AddressesPubKeyHashRequest
	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}
	resp, err := sign.AddressesPubKeyHash(&req, &cp)
	if err != nil {
		return C.CString(err.Error())
	}
	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export PsbtGetRecipients
func PsbtGetRecipients(s *C.char) *C.char {
	var req sign.Psbt
	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}
	resp, err := sign.PsbtGetRecipients(&req, &cp)
	if err != nil {
		return C.CString(err.Error())
	}
	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export PsbtSign
func PsbtSign(s *C.char) *C.char {
	var req sign.PsbtSignRequest
	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}
	resp, err := sign.PsbtSign(&req)
	if err != nil {
		return C.CString(err.Error())
	}
	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export PsbtSignPubKeyHash
func PsbtSignPubKeyHash(s *C.char) *C.char {
	var req sign.PsbtSignPubKeyHashRequest
	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}
	resp, err := sign.PsbtSignPubKeyHash(&req)
	if err != nil {
		return C.CString(err.Error())
	}
	b, _ := json.Marshal(&resp)
	return C.CString(string(b))
}

//export PsbtFinalize
func PsbtFinalize(s *C.char) *C.char {
	var req, resp sign.Psbt
	if err := json.Unmarshal([]byte(C.GoString(s)), &req); err != nil {
		return C.CString(err.Error())
	}

	p, err := psbt.NewFromRawBytes(strings.NewReader(req.PsbtB64), true)
	if err != nil {
		return C.CString(err.Error())
	}

	if err = psbt.MaybeFinalizeAll(p); err != nil {
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
