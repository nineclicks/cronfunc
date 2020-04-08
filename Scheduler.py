from CronMatch import cron_match
from datetime import datetime
from time import sleep
from threading import Thread
from threading import Lock
from threading import Event

class Scheduler:

    _running = False
    _entries = []
    _last_tick = None
    _tick_thread = None
    _lock = None
    fn = None
    _exit = None

    def __init__(self):
        self._lock = Lock()
        self.start()

    def load_cron(self, cron, fn):
        with self._lock:
            entries = cron.split('\n')
            for e in entries:
                self._entries.append((e, fn))
    
    def stop(self):
        with self._lock:
            if self._running:
                self._exit.set()
                self._running = False
                self._tick_thread = None

    def start(self):
        with self._lock:
            if self._running is False:
                self._tick_thread = Thread(target=self._tick)
                self._exit = Event()
                self._running = True
                self._tick_thread.start()

    def _check_cron(self):
        with self._lock:
            for entry in self._entries:
                cron = entry[0]
                fn = entry[1]
                match = cron_match(cron)
                if match is not False:
                    fn(match)

    def _trim_datetime(self, dt = None):
        if dt is None:
            dt = datetime.now()

        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0, 0)

    def _tick(self):
        while self._running:
            t = datetime.utcnow()
            rem = t.second + (t.microsecond / 1000000)
            self._exit.wait(60.001 - rem)

            # Make extra sure that we don't continue twice in the same minute
            while self._trim_datetime() == self._last_tick:
                self._exit.wait(.1)
            
            if self._running is False:
                break

            self._last_tick = self._trim_datetime()

            self._check_cron()

        self._running = False
        self._exit = None