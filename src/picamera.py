import time
import numpy as np
from threading import Event
from PIL import Image, ImageOps

from kivy.clock import Clock
from kivy.core.camera import Camera

PiCameraError = Exception


class PiVideoStream:
    def __init__(self, resolution, framerate, format):
        self.event = Event()
        self.image = None
        self.resolution = resolution

    def start(self):
        def f(dt):
            self.start_time = time.time()
            self.cam = Camera()
            self.cam.bind(on_texture=self.on_tex)
            self.event.set()
        Clock.schedule_once(f)
        self.event.wait()

    def on_tex(self, cam):
        if time.time() - self.start_time > 1:
            self.image = Image.frombytes(mode='RGBA', size=cam.texture.size, data=cam.texture.pixels)

    def read(self):
        if image := self.image:
            return np.array(ImageOps.flip(image.convert('RGB').resize(self.resolution)))
        return None

    def stop(self):
        def f(dt):
            self.cam.stop()
            self.event.set()
        Clock.schedule_once(f)
        self.event.wait()


class PiCamera(PiVideoStream):
    def __init__(self, resolution, framerate):
        super().__init__(resolution, framerate, 0)
        self.exposure_speed = 0
        self.awb_gains = 0

    def start_preview(self):
        self.start()

    def capture(self, stream, format):
        while True:
            frame = self.read()
            if frame is not None:
                break
            time.sleep(0.1)
        Image.fromarray(frame).save(stream, format)

    def close(self):
        self.stop()
