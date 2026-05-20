import io
import sys

def print_exception(e, limit=None, file=None, chain=True):
    sys.print_exception(e, file if file else sys.stdout)

def format_exception(e, limit=None, chain=True):
    buf = io.StringIO()
    sys.print_exception(e, buf)
    return [s + '\n' for s in buf.getvalue().splitlines()]
