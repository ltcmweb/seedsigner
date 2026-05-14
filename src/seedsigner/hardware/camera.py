import io

from gettext import gettext as _
from PIL import Image

from seedsigner.models.settings import Settings, SettingsConstants
from seedsigner.models.singleton import Singleton



class CameraConnectionError(Exception):
    pass



class Camera(Singleton):
    _video_stream = None
    _picamera = None
    _camera_rotation = None

    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only Controller
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        cls._instance._camera_rotation = int(Settings.get_instance().get_value(SettingsConstants.SETTING__CAMERA_ROTATION))
        return cls._instance


    def _start(self, resolution):
        import camera
        dim = max(resolution)
        camera.start(dim, dim)
        self._buffer = bytearray(dim * dim * 2)
        self._resolution = dim, dim
        return camera


    def start_video_stream_mode(self, resolution=(512, 384), framerate=12, format="bgr"):
        if self._video_stream is not None:
            self.stop_video_stream_mode()

        try:
            self._video_stream = self._start(resolution)
        except RuntimeError:
            # This error most often occurs because the camera connection is loose
            raise CameraConnectionError()


    def read_video_stream(self, frame: Image.Image):
        if not self._video_stream:
            raise Exception("Must call start_video_stream first.")
        if frame.width != self._resolution[0]:
            raise Exception("Frame width doesn't match camera.")
        self._video_stream.read(self._buffer)
        offset = (self._resolution[1] - frame.height) * frame.width
        frame.canvas.setbytes(memoryview(self._buffer)[offset:])


    def stop_video_stream_mode(self):
        if self._video_stream is not None:
            self._video_stream.stop()
            self._video_stream = None


    def start_single_frame_mode(self, resolution=(720, 480)):
        if self._video_stream is not None:
            self.stop_video_stream_mode()
        if self._picamera is not None:
            self._picamera.stop()

        try:
            self._picamera = self._start(resolution)
        except RuntimeError:
            # This error most often occurs because the camera connection is loose
            raise CameraConnectionError()


    def capture_frame(self):
        if self._picamera is None:
            raise Exception("Must call start_single_frame_mode first.")

        self._picamera.read(self._buffer)
        return Image.frombytes('RGB565', self._resolution, self._buffer)


    def stop_single_frame_mode(self):
        if self._picamera is not None:
            self._picamera.stop()
            self._picamera = None

