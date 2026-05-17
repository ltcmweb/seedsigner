def getrgb(color):
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
            return tuple(bytes.fromhex(color[1:]))
        elif len(color) == 4:
            return tuple(int(c * 2, 16) for c in color[1:])

def rgb_to_int(color):
    if len(color) == 3:
        color += 0xff,
    r, g, b, a = color
    return a << 24 | r << 16 | g << 8 | b

def pil_to_rgb(color, mode='RGB'):
    rgb = (
        color & 0xff,
        (color >> 8) & 0xff,
        (color >> 16) & 0xff,
    )
    if mode == 'RGBA':
        rgb += color >> 24,
    return rgb

def color_to_int(color, mode='RGB'):
    if color is None:
        return 0
    elif isinstance(color, int):
        color = pil_to_rgb(color, mode)
    elif isinstance(color, str):
        color = getrgb(color)
    return rgb_to_int(color)
