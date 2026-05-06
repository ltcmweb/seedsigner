import k_quirc

class ZBarSymbol:
    QRCODE = 1

class Decoded:
    def __init__(self, data):
        self.data = data

def decode(image, symbols=None, binary=False):
    pixels = image.tobytes()
    grayscale = bytearray()
    for i in range(0, len(pixels), 3):
        b = pixels[i]
        g = pixels[i + 1]
        r = pixels[i + 2]
        y = int(0.299 * r + 0.587 * g + 0.114 * b)
        grayscale.append(y)

    results = k_quirc.decode_grayscale(grayscale, image.width, image.height, True)
    return [Decoded(x.decode()) for x in results]
