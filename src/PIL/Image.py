from builtins import open as pyopen
import lvgl

from .ImageDraw import Draw

class Image:
    def __init__(self, canvas):
        self.canvas = canvas

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def size(self):
        return self.canvas.size()

    def convert(self, mode):
        canvas = lvgl.Canvas(mode, self.size)
        self.canvas.copyto(canvas, (0, 0))
        return Image(canvas)

    def putalpha(self, alpha):
        lvgl.putalpha(self.canvas, alpha)

    def paste(self, image, pos=(0, 0), mask=None):
        image.canvas.copyto(self.canvas, pos)

    def copy(self):
        return self.convert('RGB565')

    def tobytes(self):
        return self.canvas.tobytes()

    def resize(self, size, resample=None, box=None):
        return self.crop(box)

    def filter(self, filter):
        return self

    def crop(self, box=None):
        if box is None:
            return self
        x1, y1, x2, y2 = box
        canvas = lvgl.Canvas('RGB565', (x2 - x1, y2 - y1))
        self.canvas.copyto(canvas, (-x1, -y1))
        return Image(canvas)

def new(mode, size, color=0, visible=False):
    if mode == 'RGB':
        mode = 'RGB565'
    image = Image(lvgl.Canvas(mode, size, visible))
    if color != 0:
        Draw(image).rectangle((0, 0) + size, fill=color)
    return image

def open(name):
    return Image(lvgl.load(pyopen(name, 'rb').read()))

def frombytes(mode, size, data):
    canvas = lvgl.Canvas(mode, size)
    canvas.setbytes(data)
    return Image(canvas)

def alpha_composite(back, front):
    image = back.convert('RGBA')
    front.canvas.copyto(image.canvas, (0, 0))
    return image

class Resampling:
    NEAREST = 0
    LANCZOS = 1
    BICUBIC = 2

LANCZOS = 1
