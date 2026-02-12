package main

//#include <stdlib.h>
import "C"

import (
	"context"
	"unsafe"

	"github.com/ltcmweb/ltcd/chaincfg"
	"github.com/ltcmweb/mwebd"
	mwebdproto "github.com/ltcmweb/mwebd/proto"
	"google.golang.org/protobuf/encoding/protojson"
	"google.golang.org/protobuf/proto"
)

func doReq(req string, msg proto.Message,
	f func(s *mwebd.Server) (proto.Message, error)) string {

	if err := protojson.Unmarshal([]byte(req), msg); err != nil {
		return err.Error()
	}
	msg, err := f(mwebd.NewBareServer(chaincfg.MainNetParams))
	if err != nil {
		return err.Error()
	}
	resp, err := protojson.Marshal(msg)
	if err != nil {
		return err.Error()
	}
	return string(resp)
}

//export Addresses
func Addresses(req string) *C.char {
	msg := &mwebdproto.AddressRequest{}
	return C.CString(doReq(req, msg, func(s *mwebd.Server) (proto.Message, error) {
		return s.Addresses(context.Background(), msg)
	}))
}

//export PsbtGetRecipients
func PsbtGetRecipients(req string) *C.char {
	msg := &mwebdproto.PsbtGetRecipientsRequest{}
	return C.CString(doReq(req, msg, func(s *mwebd.Server) (proto.Message, error) {
		return s.PsbtGetRecipients(context.Background(), msg)
	}))
}

//export PsbtSign
func PsbtSign(req string) *C.char {
	msg := &mwebdproto.PsbtSignRequest{}
	return C.CString(doReq(req, msg, func(s *mwebd.Server) (proto.Message, error) {
		return s.PsbtSign(context.Background(), msg)
	}))
}

//export PsbtSignNonMweb
func PsbtSignNonMweb(req string) *C.char {
	msg := &mwebdproto.PsbtSignNonMwebRequest{}
	return C.CString(doReq(req, msg, func(s *mwebd.Server) (proto.Message, error) {
		return s.PsbtSignNonMweb(context.Background(), msg)
	}))
}

//export FreeCString
func FreeCString(s *C.char) {
	C.free(unsafe.Pointer(s))
}

func main() {}
