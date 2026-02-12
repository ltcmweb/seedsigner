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

    def sign_non_mweb(self, key, i):
        self.b64 = psbt_sign_non_mweb(self.b64, key, i)

    def serialize(self):
        return b64decode(self.b64)
