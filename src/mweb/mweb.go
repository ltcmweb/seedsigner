package main

import "C"

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/ltcmweb/ltcd/chaincfg"
	"github.com/ltcmweb/ltcd/ltcutil/psbt"
	"github.com/ltcmweb/mwebd/sign"
)

func main() {
	resp, err := makeReq(os.Args[1], os.Args[2])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	} else {
		fmt.Println(resp)
	}
}

//export mweb
func mweb(fn, req *C.char) *C.char {
	resp, err := makeReq(C.GoString(fn), C.GoString(req))
	if err != nil {
		return C.CString(err.Error())
	} else {
		return C.CString(resp)
	}
}

func doReq[Req, Resp any](f func(*Req) (Resp, error), arg string) (s string, err error) {
	var req Req
	if err = json.Unmarshal([]byte(arg), &req); err != nil {
		return
	}
	resp, err := f(&req)
	if err != nil {
		return
	}
	b, _ := json.Marshal(resp)
	return string(b), nil
}

func makeReq(fn, req string) (string, error) {
	switch fn {
	case "Addresses":
		return doReq(func(req *sign.AddressesRequest) (sign.AddressesResponse, error) {
			return sign.Addresses(req, &chaincfg.MainNetParams), nil
		}, req)
	case "AddressesPubKeyHash":
		return doReq(func(req *sign.AddressesPubKeyHashRequest) (sign.AddressesResponse, error) {
			return sign.AddressesPubKeyHash(req, &chaincfg.MainNetParams)
		}, req)
	case "PsbtGetRecipients":
		return doReq(func(req *sign.Psbt) (sign.PsbtGetRecipientsResponse, error) {
			return sign.PsbtGetRecipients(req, &chaincfg.MainNetParams)
		}, req)
	case "PsbtSign":
		return doReq(sign.PsbtSign, req)
	case "PsbtSignPubKeyHash":
		return doReq(sign.PsbtSignPubKeyHash, req)
	case "PsbtFinalize":
		return doReq(func(req *sign.Psbt) (resp sign.Psbt, err error) {
			p, err := psbt.NewFromRawBytes(strings.NewReader(req.PsbtB64), true)
			if err != nil {
				return
			}
			if err = psbt.MaybeFinalizeAll(p); err != nil {
				return
			}
			resp.PsbtB64, err = p.B64Encode()
			return
		}, req)
	}
	return "", nil
}
