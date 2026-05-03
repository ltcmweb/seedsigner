import lvgl

class ImageDraw:
    def __init__(self, image):
        self.canvas = image.canvas

    def rectangle(self, box, *, fill, outline=None, width=1):
        lvgl.rectangle(self.canvas, box, color_to_int(fill), 0)

    def rounded_rectangle(self, box, *, fill, radius, outline=None, width=1):
        lvgl.rectangle(self.canvas, box, color_to_int(fill), radius)

    def text(self, xy, text, *, font, fill, anchor):
        lvgl.text(self.canvas, xy, text, color_to_int(fill), anchor)

    def line(self, xy, fill, width=1):
        lvgl.line(self.canvas, xy, color_to_int(fill))

    def ellipse(self, box, fill, outline=None, width=1):
        pass

def Draw(image):
    return ImageDraw(image)

def color_to_int(color):
    if isinstance(color, str):
        if color == 'black':
            color = '#000000'
        if color[0] == '#':
            if len(color) == 7:
                color = int(color[1:], 16)
            elif len(color) == 4:
                color = int(''.join(c * 2 for c in color[1:]), 16)
    return color
