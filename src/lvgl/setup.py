from setuptools import setup, Extension
import glob

lvgl_sources = glob.glob("lvgl/src/**/*.c", recursive=True)

module = Extension(
    "lvgl",
    sources=["lvgl.c", "canvas.c"] + lvgl_sources,
    include_dirs=[
        "lvgl",
        "lvgl/src",
    ],
)

setup(
    name="lvgl",
    ext_modules=[module],
)
