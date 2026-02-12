from base64 import b64encode
from ctypes import *
import json
import os

lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), 'mweb'))

class string(Structure):
    _fields_ = [('p', c_char_p), ('n', c_int)]
    def __init__(self, s):
        self.b = s.encode() if isinstance(s, str) else s
        self.p = c_char_p(self.b)
        self.n = len(self.b)

def do_req(f, req):
    f.restype = c_void_p
    p = f(string(json.dumps(req)))
    s = string_at(p).decode()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        raise ValueError(s)
    finally:
        lib.FreeCString.argtypes = [c_void_p]
        lib.FreeCString(p)

def b64(b): return b64encode(b).decode()

def addresses(key, i, j):
    return do_req(lib.Addresses, {
        "scanSecret": b64(key.child(0x80000000).key.secret),
        "spendPubkey": b64(key.child(0x80000001).key.sec()),
        "fromIndex": i,
        "toIndex": j,
    })["address"]

def psbt_get_recipients(psbtB64):
    return do_req(lib.PsbtGetRecipients, {
        "psbtB64": psbtB64,
    })

def psbt_sign(psbtB64, key):
    return do_req(lib.PsbtSign, {
        "psbtB64": psbtB64,
        "scanSecret": b64(key.child(0x80000000).key.secret),
        "spendSecret": b64(key.child(0x80000001).key.secret),
    })["psbtB64"]

def psbt_sign_non_mweb(psbtB64, key, index):
    return do_req(lib.PsbtSignNonMweb, {
        "psbtB64": psbtB64,
        "privKey": b64(key),
        "index": index,
    })["psbtB64"]
