from base64 import *
from .mweb import *

class Psbt:
    @classmethod
    def parse(cls, data):
        psbt = cls()
        psbt.b64 = b64encode(data).decode()
        psbt.info = psbt_get_recipients(psbt.b64)
        psbt.inputs = []
        psbt.outputs = []
        return psbt

    def sign(self, key):
        self.b64 = psbt_sign(self.b64, key)

    def sign_pub_key_hash(self, key):
        recv = addresses_pub_key_hash(key.child(0).to_string())
        chng = addresses_pub_key_hash(key.child(1).to_string())
        for i, addr in enumerate(self.info["InputAddress"]):
            k = None
            if addr in recv:
                k = key.child(0).child(recv.index(addr))
            elif addr in chng:
                k = key.child(1).child(chng.index(addr))
            if k:
                self.b64 = psbt_sign_pub_key_hash(self.b64, k.key.secret, i)

    def serialize(self):
        return b64decode(self.b64)
