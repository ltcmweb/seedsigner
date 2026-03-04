import sys
from PIL import ImageOps

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Keyboard, Window
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget

from seedsigner.hardware import buttons
from seedsigner.hardware.displays.display_driver import BaseDisplayDriver
from seedsigner.hardware.touchbuttons import TouchButtons

buttons.HardwareButtons = TouchButtons


class _Display(BaseDisplayDriver, App):
    def __init__(self):
        self.margin_y = Window.height // 16
        width = Window.width // 3
        height = (Window.height - self.margin_y*2) // 3
        BaseDisplayDriver.__init__(self, width, height)
        App.__init__(self)
        self.do_invert = False
        self.image = None
        self.trigger = Clock.create_trigger(lambda dt: self.redraw())

    def build(self):
        self.title = 'SeedSigner'

        self.widget = Widget()
        with self.widget.canvas:
            self.rect = Rectangle(pos=(0, self.margin_y))

        self.widget.bind(size=lambda x, y: self.redraw())
        self.widget.bind(on_touch_down=lambda x, y: self.on_touch('touch_down', y))
        self.widget.bind(on_touch_move=lambda x, y: self.on_touch('touch_move', y))
        self.widget.bind(on_touch_up=lambda x, y: self.on_touch('touch_up', y))
        Window.bind(on_keyboard=self.on_keyboard)

        if hasattr(sys, 'getandroidapilevel'):
            from android.permissions import request_permission, Permission
            request_permission(Permission.CAMERA)

        return self.widget

    def invert(self, enabled = True):
        self.do_invert = enabled

    def show_image(self, image, x, y):
        self.image = image.copy()
        self.trigger()

    def redraw(self):
        if image := self.image:
            if self.do_invert:
                image = ImageOps.invert(image)
            texture = Texture.create(size=image.size, colorfmt='rgb')
            texture.flip_vertical()
            texture.blit_buffer(image.convert('RGB').tobytes())
            self.rect.texture = texture
            sx, sy = self.widget.size
            self.rect.size = sx, sy - self.margin_y*2

    def on_touch(self, op, touch):
        x, y = touch.pos
        x *= self.width / Window.width
        y = Window.height - y - self.margin_y
        y *= self.height / (Window.height - self.margin_y*2)
        hw_input = TouchButtons.get_instance()
        hw_input.queue.put((op, x, y))
        if op == 'touch_down':
            hw_input.touch_down = True
        elif op == 'touch_up':
            hw_input.touch_down = False
        return True

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        for op in ['up', 'down', 'left', 'right', '1', '2', '3', 'enter', 'escape']:
            if key == Keyboard.keycodes[op]:
                TouchButtons.get_instance().queue.put((op, 0, 0))
                return True
        return False


Display = _Display()
