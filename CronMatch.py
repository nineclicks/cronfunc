from datetime import datetime
import re

class CronMatch:
    # Full cron pattern
    _REG_CRON_FULL = r'^\s*([0-9,-\/\*]*)\s+([0-9,-\/\*]*)\s+([0-9,-\/\*]*)\s+([0-9,-\/\*]*)\s+([0-9,-\/\*]*)(?:\s*$|\s+(.*?)$)'

    # Segment pattern x-y/z
    _REG_CRON_SEG = r'^(\d+|\*)(?:(?<!\*)-(\d+))?(?:\/(\d+))?$'

    # Valid range for each segment
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
            # Cron pattern is not valid
            raise ValueError('Invalid pattern')

        groups = match.groups()
        if dt == None:
            # No datetime was provided so use now
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
                    # A segment doesn't match so the pattern doesn't match
                    return False

            if groups[5]:
                # Command was included to return it
                return groups[5]
            # No pattern so just return True
            return True

        except ValueError as _:
            raise ValueError('Invalid pattern')

    @staticmethod
    def _cron_in(n, pattern, pos):
        n = int(n)
        if pattern == '*':
            return True

        if ',' in pattern:
            # Break up list and return True if any are True
            patterns = pattern.split(',')
            for p in patterns:
                if CronMatch._cron_in(n, p, pos):
                    return True

            return False

        # Not dealing with a list by this point
        # {group0}-{group1}/{group2}
        match = re.match(CronMatch._REG_CRON_SEG, pattern)

        if match is None:
            # Invalid pattern
            raise ValueError()

        # Convert numeric groups to int type
        groups = [int(x) if (x is not None and x != '*') else x for x in match.groups()]
        valid_range = CronMatch._VALID_RANGES[pos]

        # Check that all number for this segment are a valid value (eg 0-59)
        for x in groups:
            if x is not None and x != '*' and x not in valid_range:
                raise ValueError

        if groups[1] is None and groups[0] != '*':
            # Not a range, return true if group0 matches value or false if not
            return groups[0] == n

        if groups[1] is not None:
            # Segment is an x-y range
            if groups[0] > groups[1]:
                # Range is in wrong order
                raise ValueError()

            if n not in range(groups[0], groups[1] + 1):
                # Value not in range
                return False

        # At this point, segment is a range or a * and value matches
        if groups[2] is None:
            # There is no step to check
            return True

        if n % groups[2] == 0:
            # There is a step and value is a multiple of that step
            return True

        # Value is in range but not a multiple of the step
        return False

