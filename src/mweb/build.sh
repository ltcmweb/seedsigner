#!/bin/sh

arm() {
    export CC=arm-linux-gnueabihf-gcc
    export CGO_ENABLED=1
    export GOARCH=arm
    export GOOS=linux
}

case $1 in
    pi0)
        arm
        export CGO_CFLAGS="-mcpu=arm1176jzf-s -O2"
        export GOARM=6
        ;;
    pi02w)
        arm
        export CGO_CFLAGS="-mcpu=cortex-a53 -O2"
        ;;
esac

go build -buildmode=c-shared \
         -buildvcs=false \
         -ldflags="-s -w" \
         -o mweb$1
