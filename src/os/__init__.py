# Replace built-in os module.
from uos import *

# Provide optional dependencies (which may be installed separately).
try:
    from . import path
except ImportError:
    pass

def walk(top):
    dirs, files = [], []
    for entry in ilistdir(top):
        name = entry[0]
        code = entry[1]
        if name not in ('.', '..'):
            if code & 0x4000:
                dirs.append(name)
            else:
                files.append(name)
    yield top, dirs, files
    for name in dirs:
        yield from walk(path.join(top, name))

environ = {}
