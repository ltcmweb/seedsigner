#!/bin/sh

OUTPUT=mweb

if [ "$1" = "arm" ]; then
    export CC="arm-linux-gnueabihf-gcc -march=armv6 -mfpu=vfp"
    export CGO_ENABLED=1
    export GOARCH=arm
    export GOARM=6
    export GOOS=linux
    OUTPUT=mweb-arm
fi

go build -buildmode=c-shared -ldflags="-s -w" -o $OUTPUT
