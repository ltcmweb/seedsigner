package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/ltcmweb/ltcd/chaincfg"
	"github.com/ltcmweb/ltcd/ltcutil/psbt"
	"github.com/ltcmweb/mwebd/sign"
)

func doReq[Req, Resp any](f func(*Req) (Resp, error)) {
	var req Req
	if err := json.Unmarshal([]byte(os.Args[2]), &req); err != nil {
		fmt.Fprintln(os.Stderr, err)
		return
	}
	resp, err := f(&req)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return
	}
	b, _ := json.Marshal(resp)
	fmt.Println(string(b))
}

func main() {
	switch os.Args[1] {
	case "Addresses":
		doReq(func(req *sign.AddressesRequest) (sign.AddressesResponse, error) {
			return sign.Addresses(req, &chaincfg.MainNetParams), nil
		})
	case "AddressesPubKeyHash":
		doReq(func(req *sign.AddressesPubKeyHashRequest) (sign.AddressesResponse, error) {
			return sign.AddressesPubKeyHash(req, &chaincfg.MainNetParams)
		})
	case "PsbtGetRecipients":
		doReq(func(req *sign.Psbt) (sign.PsbtGetRecipientsResponse, error) {
			return sign.PsbtGetRecipients(req, &chaincfg.MainNetParams)
		})
	case "PsbtSign":
		doReq(sign.PsbtSign)
	case "PsbtSignPubKeyHash":
		doReq(sign.PsbtSignPubKeyHash)
	case "PsbtFinalize":
		doReq(func(req *sign.Psbt) (resp sign.Psbt, err error) {
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
}
