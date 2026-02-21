from base64 import b64encode
from ctypes import *
from functools import lru_cache
import json
import os

lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), 'mweb'))
lib.FreeCString.argtypes = [c_void_p]

def do_req(f, req):
    f.restype = c_void_p
    p = f(json.dumps(req).encode())
    s = string_at(p).decode()
    lib.FreeCString(p)
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        raise ValueError(s)

def b64(b): return b64encode(b).decode()

def addresses(key, i, j):
    return do_req(lib.Addresses, {
        "Scan": b64(key.child(0x80000000).key.secret),
        "SpendPub": b64(key.child(0x80000001).key.sec()),
        "From": i,
        "To": j,
    })["Address"]

@lru_cache
def addresses_pub_key_hash(xpub, i=0, j=500):
    return do_req(lib.AddressesPubKeyHash, {
        "XPub": xpub,
        "From": i,
        "To": j,
    })["Address"]

def psbt_get_recipients(psbtB64):
    return do_req(lib.PsbtGetRecipients, {
        "PsbtB64": psbtB64,
    })

def psbt_sign(psbtB64, key):
    return do_req(lib.PsbtSign, {
        "PsbtB64": psbtB64,
        "Scan": b64(key.child(0x80000000).key.secret),
        "Spend": b64(key.child(0x80000001).key.secret),
    })["PsbtB64"]

def psbt_sign_pub_key_hash(psbtB64, key, index):
    return do_req(lib.PsbtSignPubKeyHash, {
        "PsbtB64": psbtB64,
        "PrivKey": b64(key),
        "Index": index,
    })["PsbtB64"]

def psbt_finalize(psbtB64):
    return do_req(lib.PsbtFinalize, {
        "PsbtB64": psbtB64,
    })["PsbtB64"]
