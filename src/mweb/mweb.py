from base64 import b64encode
from functools import lru_cache
import json
import os
import subprocess
import sys

def do_req(f, req):
    cmd = os.path.join(os.path.dirname(__file__), "mweb")
    req = json.dumps(req)
    if hasattr(sys, "getandroidapilevel"):
        from jnius import autoclass
        activity = autoclass("org.kivy.android.PythonActivity").mActivity
        dir = activity.getApplicationInfo().nativeLibraryDir
        cmd = os.path.join(dir, "libmweb.so")
    res = subprocess.run([cmd, f, req], capture_output=True, text=True)
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        raise ValueError(res.stderr)

def b64(b): return b64encode(b).decode()

def addresses(key, i=0, j=500):
    return _addresses(key.child(0x80000000).key.secret,
                      key.child(0x80000001).key.sec(), i, j)

@lru_cache
def _addresses(scan, spendPub, i, j):
    return do_req("Addresses", {
        "Scan": b64(scan),
        "SpendPub": b64(spendPub),
        "From": i,
        "To": j,
    })["Address"]

@lru_cache
def addresses_pub_key_hash(xpub, i=0, j=1000):
    return do_req("AddressesPubKeyHash", {
        "XPub": xpub,
        "From": i,
        "To": j,
    })["Address"]

def psbt_get_recipients(psbtB64):
    return do_req("PsbtGetRecipients", {
        "PsbtB64": psbtB64,
    })

def psbt_sign(psbtB64, key):
    return do_req("PsbtSign", {
        "PsbtB64": psbtB64,
        "Scan": b64(key.child(0x80000000).key.secret),
        "Spend": b64(key.child(0x80000001).key.secret),
    })["PsbtB64"]

def psbt_sign_pub_key_hash(psbtB64, key, index):
    return do_req("PsbtSignPubKeyHash", {
        "PsbtB64": psbtB64,
        "PrivKey": b64(key),
        "Index": index,
    })["PsbtB64"]

def psbt_finalize(psbtB64):
    return do_req("PsbtFinalize", {
        "PsbtB64": psbtB64,
    })["PsbtB64"]
