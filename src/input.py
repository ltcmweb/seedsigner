import sys
import select

from seedsigner.hardware.touchbuttons import TouchButtons
from seedsigner.models.threads import BaseThread

class InputThread(BaseThread):
    def read_key(self):
        poll = select.poll()
        poll.register(sys.stdin, select.POLLIN)

        ch = sys.stdin.read(1)
        if ch == '\n':
            return 'enter'
        if ch != '\x1b':
            return ch
        if poll.poll(50):
            ch = sys.stdin.read(1)
            if ch == '[':
                ch = sys.stdin.read(1)
                if ch == 'A': return 'up'
                if ch == 'B': return 'down'
                if ch == 'C': return 'right'
                if ch == 'D': return 'left'
        return 'escape'

    def run(self):
        while True:
            key = self.read_key()
            if key in ['up', 'down', 'left', 'right', '1', '2', '3', 'enter', 'escape']:
                TouchButtons.get_instance().queue.put_nowait((key, 0, 0))
