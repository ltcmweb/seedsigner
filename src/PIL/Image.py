from builtins import open as pyopen
import numpy as np
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
        pass

    def paste(self, image, pos=(0, 0)):
        image.canvas.copyto(self.canvas, pos)

    def copy(self):
        return self.convert('RGB')

    def tobytes(self):
        return self.canvas.tobytes()

    def resize(self, size, resample=None):
        return self

    def filter(self, filter):
        return self

    def crop(self, box):
        x1, y1, x2, y2 = box
        canvas = lvgl.Canvas('RGB', (round(x2 - x1), round(y2 - y1)))
        self.canvas.copyto(canvas, (-round(x1), -round(y1)))
        return Image(canvas)

def new(mode, size, color=0):
    image = Image(lvgl.Canvas(mode, size))
    Draw(image).rectangle((0, 0) + size, fill=color)
    return image

def open(name):
    return Image(lvgl.load(pyopen(name, 'rb').read()))

def frombytes(mode, size, data):
    canvas = lvgl.Canvas(mode, size)
    canvas.setbytes(data)
    return Image(canvas)

def fromarray(frame, mode):
    frame = np.ascontiguousarray(frame)
    canvas = lvgl.Canvas(mode, frame.shape)
    canvas.setbytes(memoryview(frame))
    return Image(canvas)

def alpha_composite(back, front):
    return front

class Resampling:
    NEAREST = 0
    LANCZOS = 1
