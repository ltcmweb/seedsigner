from dataclasses import dataclass
from PIL import Image

from seedsigner.hardware.displays.display_driver import BaseDisplayDriver

@dataclass
class LvglDisplay(BaseDisplayDriver):
    def __post_init__(self):
        self.canvas = Image.new('RGB', (self.width, self.height), visible=True)

    def show_image(self, image, x_start, y_start):
        self.canvas.paste(image, (x_start, y_start))
