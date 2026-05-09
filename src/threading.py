import _thread

_thread.stack_size(12 * 1024)


class Thread:
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        self._target = target
        self._args = args
        self._kwargs = {} if kwargs is None else kwargs
        self._is_alive = False

    def start(self):
        self._is_alive = True
        _thread.start_new_thread(self._bootstrap, ())

    def run(self):
        self._target(*self._args, **self._kwargs)

    def _bootstrap(self):
        self.run()
        self._is_alive = False

    def is_alive(self):
        return self._is_alive


Lock = _thread.allocate_lock
