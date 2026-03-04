#!/bin/sh

export CC=armv7a-linux-androideabi35-clang
export CGO_ENABLED=1
export GOARCH=arm
export GOOS=android

go build -buildvcs=false -ldflags="-s -w" -o ../../libs/android-v7/libmweb.so

export CC=aarch64-linux-android35-clang
export GOARCH=arm64

go build -buildvcs=false -ldflags="-s -w" -o ../../libs/android-v8/libmweb.so
