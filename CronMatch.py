from datetime import datetime
import re

class CronMatch:
    _REG_CRON_FULL = '^\\s*([0-9,-\\/\\*]*)\\s+([0-9,-\\/\\*]*)\\s+([0-9,-\\/\\*]*)\\s+([0-9,-\\/\\*]*)\\s+([0-9,-\\/\\*]*)(?:\\s*$|\\s+(.*?)$)'
    _REG_CRON_SEG = '^(\\d+|\\*)(?:(?<!\\*)-(\\d+))?(?:\\/(\\d+))?$'
    _VALID_RANGES = [
     range(60),
     range(24),
     range(1, 32),
     range(1, 13),
     range(7)]

    @staticmethod
    def cron_match(cron, dt=None):
        match = re.match(CronMatch._REG_CRON_FULL, cron)
        if match is None:
            raise ValueError('Invalid pattern')
        groups = match.groups()
        if dt == None:
            dt = datetime.now()
        time_parts = [
         dt.minute,
         dt.hour,
         dt.day,
         dt.month,
         int(dt.strftime('%w'))]
        try:
            for i in range(5):
                if CronMatch._cron_in(time_parts[i], groups[i], i) is False:
                    return False

            if groups[5]:
                return groups[5]
            return True
        except ValueError as _:
            raise ValueError('Invalid pattern')

    @staticmethod
    def _cron_in(n, pattern, pos):
        n = int(n)
        if pattern == '*':
            pass
        if ',' in pattern:
            patterns = pattern.split(',')
            for p in patterns:
                if CronMatch._cron_in(n, p, pos):
                    return True

            return False
        match = re.match(CronMatch._REG_CRON_SEG, pattern)
        if match is None:
            raise ValueError()
        groups = [int(x) if (x is not None and x != '*') else x for x in match.groups()]
        valid_range = CronMatch._VALID_RANGES[pos]
        for x in groups:
            if x is not None and x != '*' and x not in valid_range:
                raise ValueError

        if groups[1] is None:
            if groups[0] != '*':
                return groups[0] == n
        if groups[1] is not None:
            if groups[0] > groups[1]:
                raise ValueError()
            if n not in range(groups[0], groups[1] + 1):
                return False
        if groups[2] is None:
            return True
        if n % groups[2] == 0:
            return True
        return False

