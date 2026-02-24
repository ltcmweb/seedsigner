#!/bin/sh

OUTPUT=mweb

if [ "$1" = "arm" ]; then
    export CC=arm-linux-gnueabihf-gcc
    export CGO_CFLAGS="-mcpu=arm1176jzf-s -O2"
    export CGO_ENABLED=1
    export GOARCH=arm
    export GOARM=6
    export GOOS=linux
    OUTPUT=mweb-arm
fi

go build -buildmode=c-shared \
         -buildvcs=false \
         -ldflags="-s -w" \
         -o $OUTPUT
