# Replace built-in os module.
from uos import *

# Provide optional dependencies (which may be installed separately).
try:
    from . import path
except ImportError:
    pass

def walk(top):
    dirs, files = [], []
    for name, code, _, _ in ilistdir(top):
        if name not in ('.', '..'):
            if code & 0x4000:
                dirs.append(name)
            else:
                files.append(name)
    yield top, dirs, files
    for name in dirs:
        yield from walk(path.join(top, name))

environ = {}
