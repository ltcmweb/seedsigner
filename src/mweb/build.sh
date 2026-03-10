#!/bin/sh

export CC=arm-linux-gnueabihf-gcc
export CGO_CFLAGS="-mcpu=arm1176jzf-s -O2"
export CGO_ENABLED=1
export GOARCH=arm
export GOARM=6
export GOOS=linux

go build -buildvcs=false -ldflags="-s -w"
