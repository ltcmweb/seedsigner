import mweb_go
import queue
import struct
from threading import Thread
import time

from . import msg

class MwebThread(Thread):
    _requests = queue.Queue()

    def request(self, f, m):
        q = queue.Queue()
        self._requests.put_nowait((f, m, q))
        while True:
            if not q.empty():
                return q.get_nowait()
            time.sleep(0.1)

    def stack_size(self):
        return 24 * 1024

    def run(self):
        mweb_go.init(self.stack_size(), 512 * 1024)
        while True:
            if self._requests.empty():
                time.sleep(0.1)
                continue
            f, m, q = self._requests.get_nowait()
            q.put_nowait(mweb_go.mweb(f, m))

_thread = MwebThread()
_thread.start()

def do_req(f, m):
    resp = _thread.request(f, m)
    if isinstance(resp, str):
        raise ValueError(resp)
    return resp

_mweb_addr_cache = {}
_pkh_addr_cache = {}

def addresses(key, i=None, j=None):
    global _mweb_addr_cache
    scan = key.child(0x80000000).key.secret
    spendPub = key.child(0x80000001).key.sec()
    if i is None and j is None:
        if not (res := _mweb_addr_cache.get((scan, spendPub))):
            if len(_mweb_addr_cache) > 10:
                _mweb_addr_cache.clear()
            res = _addresses(scan, spendPub, 0, 100)
            _mweb_addr_cache[scan, spendPub] = res
        return res
    return _addresses(scan, spendPub, i, j)

def _addresses(scan, spendPub, i, j):
    res = []
    for k in range(i, j, 20):
        m = bytearray()
        msg.put_bytes(m, scan)
        msg.put_bytes(m, spendPub)
        msg.put_int(m, k)
        msg.put_int(m, min(k + 20, j))
        res.extend(msg.get_strs(do_req("Addresses", m))[0])
    return res

def addresses_pub_key_hash(xpub, i=None, j=None):
    global _pkh_addr_cache
    if i is None and j is None:
        if not (res := _pkh_addr_cache.get(xpub)):
            if len(_pkh_addr_cache) > 10:
                _pkh_addr_cache.clear()
            res = _addresses_pub_key_hash(xpub, 0, 200)
            _pkh_addr_cache[xpub] = res
        return res
    return _addresses_pub_key_hash(xpub, i, j)

def _addresses_pub_key_hash(xpub, i, j):
    res = []
    for k in range(i, j, 40):
        m = bytearray()
        msg.put_bytes(m, xpub)
        msg.put_int(m, k)
        msg.put_int(m, min(k + 40, j))
        res.extend(msg.get_strs(do_req("AddressesPubKeyHash", m))[0])
    return res

def psbt_get_recipients(psbt):
    m = bytearray()
    msg.put_bytes(m, psbt)
    m = do_req("PsbtGetRecipients", m)
    recipients, off = msg.get_recipients(m)
    inputs, off = msg.get_strs(m, off)
    fee, = struct.unpack_from("<q", m, off)
    return {
        "Recipient": recipients,
        "InputAddress": inputs,
        "Fee": fee,
    }

def psbt_sign(psbt, key):
    m = bytearray()
    msg.put_bytes(m, psbt)
    msg.put_bytes(m, key.child(0x80000000).key.secret)
    msg.put_bytes(m, key.child(0x80000001).key.secret)
    return msg.get_bytes(do_req("PsbtSign", m))[0]

def psbt_sign_pub_key_hash(psbt, key, index):
    m = bytearray()
    msg.put_bytes(m, psbt)
    msg.put_bytes(m, key)
    msg.put_int(m, index)
    return msg.get_bytes(do_req("PsbtSignPubKeyHash", m))[0]

def psbt_finalize(psbt):
    m = bytearray()
    msg.put_bytes(m, psbt)
    return msg.get_bytes(do_req("PsbtFinalize", m))[0]
