from PIL import Image, ImageDraw

class QR:
    STYLE__DEFAULT = 1
    STYLE__ROUNDED = 2
    STYLE__GRID = 3

    def __init__(self) -> None:
        self.image = None
        return

    def qrimage(self, data, width=240, height=240, border=3, style=None, background_color="#444"):
        box_size = 5
        qr = qrcode.QRCode( version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border=border )
        qr.add_data(data)
        qr.make(fit=True)
        if not style or style == QR.STYLE__DEFAULT:
            return qr.make_image(fill_color="black", back_color=background_color).resize((width,height)).convert('RGBA')
        else:
            if style == QR.STYLE__ROUNDED:
                qr_image = qr.make_image(
                    fill_color="black",
                    back_color=background_color,
                    image_factory=StyledPilImage,
                    module_drawer=CircleModuleDrawer()
                )

                qr_image_width, _ = qr_image.size
                qr_code_dims = int(qr_image_width / box_size) - 2*border

                if qr_code_dims > 21:
                    # The ROUNDED style mis-renders the small lower-right registration box in 25x25
                    # and 29x29.
                    draw = ImageDraw.Draw(qr_image)
                    if qr_code_dims == 25:
                        # registration block starts at 16, 16 and is 5x5
                        starting_point = 16 + border

                    elif qr_code_dims == 29:
                        # The registration block starts at 20,20 and is 5x5
                        starting_point = 20 + border
                    
                    else:
                        raise Exception(f"Unrecognized qrimage size: {qr_code_dims}")
                    
                    # Render black rectangular lines on top of the qr_image to square off
                    # the registration block.
                    lines = [
                        (
                            # top
                            (starting_point*box_size, starting_point*box_size),
                            (starting_point*box_size + 5*box_size - 1, starting_point*box_size + box_size - 1)
                        ),
                        (
                            # right
                            (starting_point*box_size + 4*box_size, starting_point*box_size),
                            (starting_point*box_size + 5*box_size - 1, starting_point*box_size + 5*box_size - 1)
                        ),
                        (
                            # left
                            (starting_point*box_size, starting_point*box_size),
                            (starting_point*box_size + box_size - 1, starting_point*box_size + 5*box_size - 1)
                        ),
                        (
                            # bottom
                            (starting_point*box_size + box_size, starting_point*box_size + 4*box_size),
                            (starting_point*box_size + 5*box_size - 1, starting_point*box_size + 5*box_size - 1)
                        ),
                        (
                            # center dot
                            (starting_point*box_size + 2*box_size, starting_point*box_size + 2*box_size),
                            (starting_point*box_size + 3*box_size - 1, starting_point*box_size + 3*box_size - 1)
                        )
                    ]

                    for line in lines:
                        draw.rectangle(line, fill="black")
                
                return qr_image.resize((width,height)).convert('RGBA')

            elif style == QR.STYLE__GRID:
                return qr.make_image(
                    fill_color="black",
                    back_color=background_color,
                    image_factory=StyledPilImage,
                    module_drawer=GappedSquareModuleDrawer()
                ).resize((width,height)).convert('RGBA')


    def qrimage_c(self, data, width=240, height=240, border=3):
        import qrcode_c
        data = qrcode_c.encode_to_string(data)
        rows = data.splitlines()
        qr_w, qr_h = len(rows[0]) + border * 2, len(rows) + border * 2
        scale_x, scale_y = width // qr_w, height // qr_h
        x_off = (width - qr_w * scale_x) // 2 + border * scale_x
        y_off = (height - qr_h * scale_y) // 2 + border * scale_y
        if not self.image or self.image.size != (width, height):
            self.image = Image.new('RGB565', (width, height))
        qrcode_c.encode_to_rgb565(self.image.tobytes(), data + '\n\0', width,
                                  scale_x, scale_y, y_off * width + x_off)
        return self.image


    def qrimage_io(self, data, width=240, height=240, border=3, background_color="808080"):
        if 1 <= border <= 10:
            border_str = str(border)
        else:
            border_str = "3"

        cmd = f"""qrencode -m {border_str} -s 3 -l L --foreground=000000 --background={background_color} -t PNG -o "/tmp/qrcode.png" "{str(data)}" """
        rv = 1

        # if qrencode fails, fall back to only encoder
        if rv != 0:
            return self.qrimage_c(data,width,height,border)
        img = Image.open("/tmp/qrcode.png").resize((width,height), Image.Resampling.NEAREST).convert("RGBA")

        return img
