#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest as ut
import datetime as dt
import tasks


class ParseRecordTest(ut.TestCase):
    @ut.skip("test_incorrect_line")
    def test_incorrect_line(self):
        line = 'Quantenna FAE4 LAPTOP-Q6ADI2G2 LAPTOP-Q6ADI2G2 (v2010.1008) (license-server-17/31495 2408), start Mon 9/24 5:34'
        self.match_feature_object(tasks.parse_record(line, 2018), 'Quantenna FAE4', 'LAPTOP-Q6ADI2G2', 'LAPTOP-Q6ADI2G2', 0,
                                  dt.datetime(2018, 9, 24, 5, 34), 0, None)

    def test_line(self):
        line = 'autodev AUTO-08 AUTO-08 (v2010.1008) (license-server-17/31495 24701), start Mon 9/17 7:27'
        self.match_feature_object(tasks.parse_record(line, 2018), 'autodev', 'AUTO-08', 'AUTO-08', 0,
                                  dt.datetime(2018, 9, 17, 7, 27), 0, None)

    def test_line_with_linger(self):
        line = 'autodev cnqoffice cnqoffice (v2015.0420) (license-server-17/31495 3401), start Mon 9/17 7:25 (linger: 2597880)'
        self.match_feature_object(tasks.parse_record(line, 2018), 'autodev', 'cnqoffice', 'cnqoffice', 0,
                                  dt.datetime(2018, 9, 17, 7, 25), 2597880,
                                  dt.datetime(2018, 9, 17, 7, 25) + dt.timedelta(seconds=2597880))

    def test_line_with_lic_count(self):
        line = 'autodev Ru-SQA-Qbox9 Ru-SQA-Qbox9 (v2015.0420) (license-server-17/31495 33019), start Thu 9/20 19:12, 200 licenses'
        self.match_feature_object(tasks.parse_record(line, 2018), 'autodev', 'Ru-SQA-Qbox9', 'Ru-SQA-Qbox9', 200,
                                  dt.datetime(2018, 9, 20, 19, 12), 0, None)

    def test_line_with_lic_count_and_linger(self):
        line = 'autodev cnqoffice cnqoffice (v2015.0420) (license-server-17/31495 3801), start Mon 9/17 7:25, 50 licenses (linger: 2597820)'
        self.match_feature_object(tasks.parse_record(line, 2018), 'autodev', 'cnqoffice', 'cnqoffice', 50,
                                  dt.datetime(2018, 9, 17, 7, 25), 2597820,
                                  dt.datetime(2018, 9, 17, 7, 25) + dt.timedelta(seconds=2597820))

    def match_feature_object(self, _feature, _user, _host, _display, _lic_count, _start_datetime, _linger,
                             _end_datetime):
        self.assertIsNotNone(_feature)
        self.assertEqual(_feature.m_user, _user)
        self.assertEqual(_feature.m_host, _host)
        self.assertEqual(_feature.m_display, _display)
        self.assertEqual(_feature.m_lic_count, _lic_count)
        self.assertEqual(_feature.m_start_datetime, _start_datetime)
        self.assertEqual(_feature.m_linger, _linger)
        self.assertEqual(_feature.m_end_datetime, _end_datetime)


class FeatureRecordEqualityTest(ut.TestCase):
    def test_equal(self):
        fr1 = tasks.FeatureRecord('user', 'host', 'display', 2017, 10, 11, 12, 1, 2, 3)
        fr2 = tasks.FeatureRecord('user', 'host', 'display', 2018, 9, 12, 14, 0, 0, 0)
        self.assertEqual(fr1, fr2)
        self.assertEqual(hash(fr1), hash(fr2))

    def test_not_equal(self):
        fr1 = tasks.FeatureRecord('user', 'host', 'display', 2017, 10, 11, 12, 1, 2, 3)
        fr2 = tasks.FeatureRecord('user1', 'host', 'display', 2017, 10, 11, 12, 1, 2, 3)
        fr3 = tasks.FeatureRecord('user', 'host1', 'display', 2017, 10, 11, 12, 1, 2, 3)
        fr4 = tasks.FeatureRecord('user', 'host', 'display1', 2017, 10, 11, 12, 1, 2, 3)
        for fr in [fr2, fr3, fr4]:
            self.assertNotEqual(fr1, fr)
            self.assertNotEqual(hash(fr1), hash(fr))


if __name__ == '__main__':
    ut.main()
