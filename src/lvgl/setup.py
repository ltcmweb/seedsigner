from setuptools import setup, Extension
from glob import glob

lvgl_sources = glob("lvgl/src/**/*.c", recursive=True)
fonts = glob("seedsigner-c-modules/components/seedsigner/fonts/*.c")

module = Extension(
    "lvgl",
    sources=["lvgl.c", "canvas.c"] + lvgl_sources + fonts,
    include_dirs=[
        "lvgl",
        "lvgl/src",
    ],
)

setup(
    name="lvgl",
    ext_modules=[module],
)
