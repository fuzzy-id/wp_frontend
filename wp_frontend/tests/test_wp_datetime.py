# -*- coding: utf-8 -*-
import unittest
from wp_frontend.views import wp_datetime
import datetime

class TimeSpanWithResolutionTests(unittest.TestCase):

    def test_ms_are_cutted_from_start(self):
        span_with_resolution = wp_datetime.TimespanWithResolution()
        span_with_resolution.start = datetime.datetime(2011, 10, 22, 19, 36, 55, 19)
        expected = datetime.datetime(2011, 10, 22, 19, 36, 55)
        actual = span_with_resolution.start
        self.assertEqual(actual, expected)

    def test_ms_are_cutted_from_end(self):
        span_with_resolution = wp_datetime.TimespanWithResolution()
        span_with_resolution.end = datetime.datetime(2011, 10, 22, 19, 36, 55, 19)
        expected = datetime.datetime(2011, 10, 22, 19, 36, 55)
        actual = span_with_resolution.end
        self.assertEqual(actual, expected)

    def test_iteration_with_end_before_start(self):
        pass

    def test_avg_timespan_iterator(self):
        span_with_resolution = wp_datetime.TimespanWithResolution()
        span_with_resolution.start = datetime.datetime(2011, 10, 02, 19, 36, 55)
        span_with_resolution.end = datetime.datetime(2011, 10, 22, 19, 36, 55)
        span_with_resolution.resolution = 40
        expected = [(1317577015, 1317620215), (1317620215, 1317663415),
                    (1317663415, 1317706615), (1317706615, 1317749815),
                    (1317749815, 1317793015), (1317793015, 1317836215),
                    (1317836215, 1317879415), (1317879415, 1317922615),
                    (1317922615, 1317965815), (1317965815, 1318009015),
                    (1318009015, 1318052215), (1318052215, 1318095415),
                    (1318095415, 1318138615), (1318138615, 1318181815),
                    (1318181815, 1318225015), (1318225015, 1318268215),
                    (1318268215, 1318311415), (1318311415, 1318354615),
                    (1318354615, 1318397815), (1318397815, 1318441015),
                    (1318441015, 1318484215), (1318484215, 1318527415),
                    (1318527415, 1318570615), (1318570615, 1318613815),
                    (1318613815, 1318657015), (1318657015, 1318700215),
                    (1318700215, 1318743415), (1318743415, 1318786615),
                    (1318786615, 1318829815), (1318829815, 1318873015),
                    (1318873015, 1318916215), (1318916215, 1318959415),
                    (1318959415, 1319002615), (1319002615, 1319045815),
                    (1319045815, 1319089015), (1319089015, 1319132215),
                    (1319132215, 1319175415), (1319175415, 1319218615),
                    (1319218615, 1319261815), (1319261815, 1319305015)]
        actual = [ x for x in span_with_resolution ]
        self.assertEquals(expected, actual)
