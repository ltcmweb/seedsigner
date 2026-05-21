from dataclasses import dataclass, field
from PIL import Image
import lvgl

from seedsigner.hardware.displays.display_driver import BaseDisplayDriver

@dataclass
class LvglDisplay(BaseDisplayDriver):
    _width: int = field(1, default=lvgl.screen_size()[0])
    _height: int = field(2, default=lvgl.screen_size()[1])

    def __post_init__(self):
        self.canvas = Image.new('RGB', (self.width, self.height), visible=True)

    def invert(self, enabled):
        lvgl.invert(enabled)

    def show_image(self, image, x_start, y_start):
        self.canvas.paste(image, (x_start, y_start))
