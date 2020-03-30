from CronMatch import CronMatch
from datetime import datetime
from time import sleep

class Scheduler:

    _running = True
    _last_tick = None

    def __init__(self):
        self._tick()
        pass

    def load_cron(self, cron):
        pass

    def _check_cron(self):
        print("check cron")
        print(datetime.utcnow().microsecond / 1000000)
        pass

    def _trim_datetime(self, dt = None):
        if dt is None:
            dt = datetime.now()

        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0, 0)

    def _tick(self):

        while self._running:
            t = datetime.utcnow()
            rem = t.second + (t.microsecond / 1000000)
            sleep(60.001 - rem)

            # Make extra sure that we don't continue twice in the same minute
            while self._trim_datetime() == self._last_tick:
                sleep(.1)

            self._last_tick = self._trim_datetime()

            self._check_cron()

if __name__ == '__main__':
    s = Scheduler()
