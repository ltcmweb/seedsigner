import lvgl
import queue
import time

from seedsigner.hardware.buttons import HardwareButtonsConstants
from seedsigner.models.singleton import Singleton


def lvgl_input_cb(op, x, y):
    LV_EVENT_PRESSING = 2
    LV_EVENT_RELEASED = 11

    hw_input = TouchButtons.get_instance()
    if op == LV_EVENT_PRESSING:
        op = 'touch_move' if hw_input.touch_down else 'touch_down'
        hw_input.touch_down = True
    if op == LV_EVENT_RELEASED:
        op = 'touch_up'
        hw_input.touch_down = False
    hw_input.queue.put_nowait((op, x, y, time.time()))


class TouchButtons(Singleton):
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.queue = queue.Queue()
        self.last_input_time = int(time.time() * 1000)
        lvgl.register_input_cb(lvgl_input_cb)

    def add_button(self, button):
        self._buttons.append(button)

    def get_button(self, multi=False):
        if not multi and self._button:
            return self._button[0]
        return self._button

    def get_last_pos(self):
        return self._last_pos

    def clear(self):
        self._button = []
        self._buttons = []
        self._last_pos = 0, 0
        self.touch_down = False

    def _check_button(self, x, y):
        result = []
        for button in self._buttons:
            l = button.screen_x
            r = l + button.width
            t = button.screen_y - button.scroll_y
            b = t + button.height
            if l < x < r and t < y < b:
                result.append(button)
        return result

    def wait_for(self, keys=[]) -> int:
        from seedsigner.controller import Controller
        controller = Controller.get_instance()
        self.override_ind = False

        while True:
            if self.override_ind:
                self.override_ind = False
                return HardwareButtonsConstants.OVERRIDE

            cur_time = int(time.time() * 1000)
            if cur_time - self.last_input_time > controller.screensaver_activation_ms and controller.is_screensaver_start_allowed:
                controller.start_screensaver()
                self.update_last_input_time()
                continue

            try:
                op, x, y, t = self.queue.get_nowait()
            except queue.Empty:
                time.sleep(0.1)
                continue
            if time.time() - t > 0.2:
                continue
            self.update_last_input_time()

            if result := {
                'up': HardwareButtonsConstants.KEY_UP,
                'down': HardwareButtonsConstants.KEY_DOWN,
                'left': HardwareButtonsConstants.KEY_LEFT,
                'right': HardwareButtonsConstants.KEY_RIGHT,
                '1': HardwareButtonsConstants.KEY1,
                '2': HardwareButtonsConstants.KEY2,
                '3': HardwareButtonsConstants.KEY3,
                'enter': HardwareButtonsConstants.KEY_PRESS,
                'escape': HardwareButtonsConstants.KEY_BACK,
            }.get(op):
                self._button = []

            elif op == 'touch_down':
                self._button = self._check_button(x, y)
                self.down_pos = x, y
                self._last_pos = x, y
                if self._button:
                    result = HardwareButtonsConstants.TOUCH_DOWN

            elif op == 'touch_move':
                self.move_delta = round(x - self._last_pos[0]), round(y - self._last_pos[1])
                self._last_pos = x, y
                result = HardwareButtonsConstants.TOUCH_MOVE

            elif op == 'touch_up':
                if self._button:
                    if abs(x - self.down_pos[0]) < 5 and abs(y - self.down_pos[1]) < 5:
                        result = HardwareButtonsConstants.KEY_PRESS

            if result in keys:
                return result

    def update_last_input_time(self):
        self.last_input_time = int(time.time() * 1000)

    def trigger_override(self):
        self.override_ind = True

    def has_any_input(self) -> bool:
        try:
            result = self.touch_down
            while True:
                op, x, y, t = self.queue.get_nowait()
                if time.time() - t > 0.2:
                    continue
                if not op.startswith('touch_'):
                    result = True
                self.update_last_input_time()
                self._last_pos = x, y
        except queue.Empty:
            return result
