import lvgl

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

def color_to_int(color):
    if color is None:
        return 0
    if isinstance(color, int):
        color = color, color, color
    if isinstance(color, str):
        if color == 'black':
            color = '#000000'
        elif color == 'red':
            color = '#ff0000'
        elif color == 'orange':
            color = '#ffa500'
        elif color == 'blue':
            color = '#0000ff'
        elif color == 'white':
            color = '#ffffff'
        if color[0] == '#':
            if len(color) == 7:
                color = tuple(bytes.fromhex(color[1:]))
            elif len(color) == 4:
                color = tuple(int(c * 2, 16) for c in color[1:])
    if isinstance(color, tuple):
        if len(color) == 3:
            color += 0xff,
        r, g, b, a = color
        color = a << 24 | r << 16 | g << 8 | b
    return color
