#!/usr/bin/env python3
import unittest
import json
from datetime import datetime
from CronMatch import CronMatch

class TestStringMethods(unittest.TestCase):

    def test_datetime_now(self):
        cron = '* * * * *'
        self.assertTrue(CronMatch.cron_match(cron), 'Match datetime now')

    def test_value_error(self):
        cases = self.get_cases()['invalid_cases']
        for cron in cases:
            with self.subTest(cron=cron):
                self.assertRaises(ValueError, CronMatch.cron_match, cron)

    def test_return_command(self):
        dt = datetime(2020,1,1,0,0,0)
        command = 'one two three'
        cron = '0 0 * * * {}'.format(command)
        self.assertEqual(command, CronMatch.cron_match(cron, dt))
        cron = '0 1 * * * {}'.format(command)
        self.assertFalse(CronMatch.cron_match(cron, dt))

    def get_cases(self):
        with open('cases.json') as fp:
            cases = json.load(fp)

        return cases

    def test_cases(self):
        dt_format = '%Y/%m/%d %H:%M:%S'
        cases = self.get_cases()['valid_cases']
        for case in cases:
            cron = case['cron']
            matches = case['match']
            nomatches = case['nomatch']

            for match in matches:
                with self.subTest(cron=cron, match=match):
                    dt = datetime.strptime(match, dt_format)
                    self.assertTrue(CronMatch.cron_match(cron, dt))

            for no_match in nomatches:
                with self.subTest(cron=cron, no_match=no_match):
                    dt = datetime.strptime(no_match, dt_format)
                    self.assertFalse(CronMatch.cron_match(cron, dt))

if __name__ == '__main__':
    unittest.main()
