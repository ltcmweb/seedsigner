from pathlib import Path
import lvgl

class FreeTypeFont:
    def __init__(self, path, size):
        self.name = Path(path).stem + f'-{size}'

    def getbbox(self, text, *, anchor='lt'):
        return lvgl.text(lvgl.Canvas('RGB', (0, 0)), (0, 0),
                         text.replace('\n', ' '), self.name, 0, anchor, 0, 0)

def truetype(path, size):
    return FreeTypeFont(path, size)
