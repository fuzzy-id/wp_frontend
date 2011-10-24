# -*- coding: utf-8 -*-
import datetime
import random
from wp_frontend.models import get_data
from wp_frontend.models.calculations import calc_currKW
from wp_frontend.tests import BaseTestWithDB, strip_ms
from wp_frontend.views import wp_datetime


class PulledDataTest(BaseTestWithDB):

    def _make_the_class(self, *args):
        return get_data.PulledData(*args)

    def test_default_values_are_setted(self):
        self._add_one({})
        cols = ['version', 'datum_version', 'betriebsmodus',
                'temp_aussen']
        entry = get_data.PulledData.get_latest(self.session, cols)
        self.assertEqual(entry[0], 0)
        self.assertEqual(entry[1], datetime.date.min)
        self.assertEqual(entry[2], '')
        self.assertEqual(entry[3], 0.0)

    def test_add_one_and_get_latest_work(self):
        columns_and_values = {'temp_aussen': 24,
                              'temp_WW': 80.34 }
        self._add_one(columns_and_values)
        entry = get_data.PulledData.get_latest(self.session,
                                               columns_and_values.keys())
        self.assertEqual(entry[0], 24)
        self.assertEqual(entry[1], 80.34)

    def test_datetime_of_entry(self):
        self._add_one({})
        dt_after = strip_ms(datetime.datetime.now())
        entry = get_data.PulledData.get_latest(self.session, ['tsp'])
        entry_date = datetime.datetime.fromtimestamp(entry[0])
        self.assertEquals(dt_after, entry_date)

    def test_get_values_in_timespan_with_avg(self):
        span_with_resolution = wp_datetime.TimespanWithResolution()

        expected = {}

        for avg_start, avg_end in span_with_resolution:
            temp_aussen_sum = 0
            temp_Vl_sum = 0
            tsp_sum = 0
            count = 0
            
            for i in range(10):
                temp_aussen = random.randint(-10, 50)
                temp_Vl = random.randint(-10, 50)
                tsp = random.randint(avg_start, avg_end)
                
                temp_aussen_sum += temp_aussen
                temp_Vl_sum += temp_Vl
                tsp_sum += tsp
                
                count += 1
                entry = {'tsp': tsp,
                         'temp_aussen': temp_aussen,
                         'temp_Vl': temp_Vl}
                self._add_one(entry)
                
            avg_tsp = int(1.0*tsp_sum/count)
            expected[avg_tsp] = (1.0*temp_aussen_sum/count,
                                 calc_currKW(1.0*temp_Vl_sum/count), )

        number, entries = get_data.PulledData.get_values_in_timespan(
            self.session, ['tsp', 'temp_aussen', 'currKW'], span_with_resolution)

        self.assertEquals(number, quantity)
        
        for entry in entries:
            res_tsp = int(entry[0])
            self.assertTrue(res_tsp in expected)
            self.assertEquals(entry[1], expected[res_tsp][0])
            self.assertEquals(entry[2], expected[res_tsp][1])
        
    def test_get_values_in_timespan_wo_avg(self):
        span_with_resolution = wp_datetime.TimespanWithResolution()
        span_with_resolution.start = datetime.datetime.min
        span_with_resolution.end = span_with_resolution.start + datetime.timedelta(days=10)
        span_with_resolution.resolution = 100

        expected = {}

        for avg_start, avg_end in span_with_resolution:
            tsp = (avg_start + avg_end) / 2.0
            temp_aussen = random.randint(-10, 50)
            temp_Vl = random.randint(-10, 50)
                
            entry = {'tsp': tsp,
                     'temp_aussen': temp_aussen,
                     'temp_Vl': temp_Vl}

            self._add_one(entry)
                
            expected[tsp] = (temp_aussen,
                             calc_currKW(temp_Vl), )

        number, entries = get_data.PulledData.get_values_in_timespan(
            self.session, ['tsp', 'temp_aussen', 'currKW'], span_with_resolution)

        self.assertEquals(number, span_with_resolution.resolution)
        
        for entry in entries:
            res_tsp = int(entry[0])
            self.assertTrue(res_tsp in expected)
            self.assertEquals(entry[1], expected[res_tsp][0])
            self.assertEquals(entry[2], expected[res_tsp][1])
        
    def _test_calculated_entries(self, entry, test_column, expected):
        self._add_one(entry)
        result = get_data.PulledData.get_latest(self.session, [test_column])
        self.assertEquals(result[0], expected)

    def test_get_calculated_currKW(self):
        column = 'temp_Vl'
        entry = {column: 18.0}
        expected = 18.0 * 0.06 + 0.5
        self._test_calculated_entries(entry, 'currKW', expected)

    def test_get_deltaVlRl(self):
        entry = {'temp_Vl': 18.0,
                 'temp_Rl': 14.4}
        expected = 18.0 - 14.4
        self._test_calculated_entries(entry, 'deltaVlRl', expected)

    def test_get_deltaWQea(self):
        entry = {'temp_WQein': 12.5,
                 'temp_WQaus': 10.0}
        expected = 12.5 - 10.0
        self._test_calculated_entries(entry, 'deltaWQea', expected)
