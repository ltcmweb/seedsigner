module github.com/ltcmweb/seedsigner/src/mweb

go 1.24.0

require (
	github.com/ltcmweb/ltcd v0.25.12
	github.com/ltcmweb/mwebd/sign v0.1.0
)

require (
	github.com/btcsuite/btclog v1.0.0 // indirect
	github.com/decred/dcrd/crypto/blake256 v1.1.0 // indirect
	github.com/decred/dcrd/dcrec/secp256k1/v4 v4.4.0 // indirect
	github.com/ltcmweb/ltcd/btcec/v2 v2.3.3 // indirect
	github.com/ltcmweb/ltcd/chaincfg/chainhash v1.0.3 // indirect
	github.com/ltcmweb/secp256k1 v0.1.5 // indirect
	golang.org/x/crypto v0.48.0 // indirect
	golang.org/x/sys v0.41.0 // indirect
	lukechampine.com/blake3 v1.4.1 // indirect
)

replace lukechampine.com/blake3 => github.com/ltcmweb/blake3 v1.4.1-tinygo
