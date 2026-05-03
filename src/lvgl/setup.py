from setuptools import setup, Extension
from glob import glob

sources = glob("*.c")
lvgl_sources = glob("lvgl/src/**/*.c", recursive=True)
fonts = glob("seedsigner-c-modules/components/seedsigner/fonts/*.c")

module = Extension(
    "lvgl",
    sources=sources + lvgl_sources + fonts,
    include_dirs=[
        "lvgl",
        "lvgl/src",
    ],
)

setup(
    name="lvgl",
    ext_modules=[module],
)
