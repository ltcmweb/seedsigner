from base64 import b64encode
import json
import mweb_go
import queue
from threading import Thread
import time

class MwebThread(Thread):
    _requests = queue.Queue()

    def request(self, f, req):
        q = queue.Queue()
        self._requests.put_nowait((f, req, q))
        while True:
            try:
                return q.get_nowait()
            except queue.Empty:
                time.sleep(0.1)

    def stack_size(self):
        return 24 * 1024

    def run(self):
        mweb_go.init(self.stack_size(), 500000)
        while True:
            try:
                f, req, q = self._requests.get_nowait()
                q.put_nowait(mweb_go.mweb(f, req))
            except queue.Empty:
                time.sleep(0.1)

_thread = MwebThread()
_thread.start()

def do_req(f, req):
    res = _thread.request(f, json.dumps(req))
    try:
        return json.loads(res)
    except ValueError:
        raise ValueError(res)

def b64(b): return b64encode(b).decode()

def addresses(key, i=0, j=100):
    return _addresses(key.child(0x80000000).key.secret,
                      key.child(0x80000001).key.sec(), i, j)

def _addresses(scan, spendPub, i, j):
    res = []
    for k in range(i, j, 20):
        res.extend(do_req("Addresses", {
            "Scan": b64(scan),
            "SpendPub": b64(spendPub),
            "From": k,
            "To": min(k + 20, j),
        })["Address"])
    return res

def addresses_pub_key_hash(xpub, i=0, j=200):
    res = []
    for k in range(i, j, 40):
        res.extend(do_req("AddressesPubKeyHash", {
            "XPub": xpub,
            "From": k,
            "To": min(k + 40, j),
        })["Address"])
    return res

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
