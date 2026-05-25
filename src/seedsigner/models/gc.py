import gc
import time

from seedsigner.models.singleton import Singleton
from seedsigner.models.threads import BaseThread


class Gc(Singleton):
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            gc = cls._instance = cls.__new__(cls)
            gc._thread = GcThread()
            gc._thread.start()
        return cls._instance

    def pause(self):
        self._thread.paused = True

    def resume(self):
        self._thread.paused = False


class GcThread(BaseThread):
    def __init__(self):
        super().__init__()
        self.paused = False

    def run(self):
        while self.keep_running:
            if not self.paused:
                gc.collect()
            time.sleep(5)
