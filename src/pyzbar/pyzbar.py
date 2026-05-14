import k_quirc

class ZBarSymbol:
    QRCODE = 1

class Decoded:
    def __init__(self, data):
        self.data = data

def decode(image, symbols=None, binary=False):
    results = k_quirc.decode_rgb565(image.tobytes(), image.width, image.height, True)
    return [Decoded(x.decode()) for x in results]
