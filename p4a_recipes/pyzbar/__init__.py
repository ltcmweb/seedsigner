import os

from pythonforandroid.recipes.pyzbar import PyZBarRecipe
from pythonforandroid.util import load_source

util = load_source('util', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util.py'))


class PyZBarRecipePinned(util.InheritedRecipeMixin, PyZBarRecipe):
    version = "c3c237821c6a20b17953efe59b90df0b514a1c03"
    url = "https://github.com/seedsigner/pyzbar/archive/{version}.zip"
    sha512sum = "2e94789387fe480f24c8b3b4b3396238c7e56173f4d8d9b356f5cb42d21c6e56ae65789eace05c9891dacde79181954018eab50019e7ac6c27863d0b186999b5"


recipe = PyZBarRecipePinned()
