from pathlib import Path
from math import ceil
import lvgl

class FreeTypeFont:
    def __init__(self, path, size):
        self.name = Path(path).stem + f'-{size}'

    def getbbox(self, text, *, anchor='lt'):
        x1, y1 = 0, 0
        x2, y2 = lvgl.text(lvgl.Canvas('RGB', (0, 0)), (0, 0), text, self.name, 0, anchor)
        if anchor[1] == 's':
            dy = ceil(y2 / 4)
            y1 = dy - y2
            y2 = dy
        return x1, y1, x2, y2

def truetype(path, size):
    return FreeTypeFont(path, size)
