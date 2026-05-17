import lvgl

from .ImageColor import color_to_int

class ImageDraw:
    def __init__(self, image):
        self.canvas = image.canvas

    def rectangle(self, box, *, fill, outline=None, width=1):
        if len(box) == 2:
            box = box[0] + box[1]
        lvgl.rectangle(self.canvas, box, color_to_int(fill), color_to_int(outline), width, 0)

    def rounded_rectangle(self, box, *, fill, radius, outline=None, width=1):
        if len(box) == 2:
            box = box[0] + box[1]
        lvgl.rectangle(self.canvas, box, color_to_int(fill), color_to_int(outline), width, radius)

    def text(self, xy, text, *, font, fill, anchor="lt", stroke_width=0, stroke_fill=None):
        lvgl.text(self.canvas, xy, text, font.name, color_to_int(fill),
                  anchor, stroke_width, color_to_int(stroke_fill))

    def line(self, xy, fill=None, width=0, joint=None):
        lvgl.line(self.canvas, xy, color_to_int(fill))

    def arc(self, box, start, end, fill, width):
        lvgl.arc(self.canvas, box, start, end, color_to_int(fill), width)

    def ellipse(self, box, fill, outline=None, width=1):
        if len(box) == 2:
            box = box[0] + box[1]
        x1, y1, x2, y2 = box
        radius = min(x2 - x1 + 1, y2 - y1 + 1) // 2
        lvgl.rectangle(self.canvas, box, color_to_int(fill), color_to_int(outline), width, radius)

    def textbbox(self, xy, text, font, anchor):
        x, y = xy
        x1, y1, x2, y2 = font.getbbox(text, anchor=anchor)
        return x1 + x, y1 + y, x2 + x, y2 + y

def Draw(image):
    return ImageDraw(image)
