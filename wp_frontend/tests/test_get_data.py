# -*- coding: utf-8 -*-
import datetime
import random
from wp_frontend.models import get_data
from wp_frontend.models.calculations import CurrKW
from wp_frontend.tests import BaseTestWithDB
from wp_frontend.tests import create_entries
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
        dt_before = wp_datetime.strip_ms(datetime.datetime.now())
        self._add_one({})
        dt_after = wp_datetime.strip_ms(datetime.datetime.now())
        entry = get_data.PulledData.get_latest(self.session, ['tsp'])
        entry_date = datetime.datetime.fromtimestamp(entry[0])
        self.assertTrue(entry_date >= dt_before)
        self.assertTrue(dt_after >= entry_date)

    def test_get_values_in_timespan_with_avg(self):
        create_entries.add_get_data_entries_to_db(self.transaction, self.session)

        span_with_resolution = wp_datetime.TimespanWithResolution(
            start=create_entries.entries_start,
            end=create_entries.entries_end,
            resolution=10)

        expected = {}

        for expected_entry in range( 2, 50, 5):
            row = create_entries.get_data_entries[expected_entry]
            expected[row['tsp']] = ( row['temp_aussen'], CurrKW.calc(row['temp_Vl']), )

        entries = get_data.PulledData.get_values_in_timespan(
            self.session, ['tsp', 'temp_aussen', 'currKW'], span_with_resolution)

        self.assertEquals(10, span_with_resolution.resolution)

        for entry in entries:
            res_tsp = int(entry[0])
            self.assertTrue(res_tsp in expected)
            self.assertEquals(entry[1], expected[res_tsp][0])
            self.assertEquals(entry[2], expected[res_tsp][1])
        
    def test_get_values_in_timespan_wo_avg(self):
        create_entries.add_get_data_entries_to_db(self.transaction, self.session)

        span_with_resolution = wp_datetime.TimespanWithResolution(
            start=create_entries.entries_start,
            end=create_entries.entries_end,
            resolution=len(create_entries.get_data_entries))

        expected = {}
        for row in create_entries.get_data_entries:
            expected[row['tsp']] = ( row['temp_aussen'], CurrKW.calc(row['temp_Vl']), )

        entries = get_data.PulledData.get_values_in_timespan(
            self.session, ['tsp', 'temp_aussen', 'currKW'], span_with_resolution)

        self.assertEquals(span_with_resolution.resolution, 
                          len(create_entries.get_data_entries))
        
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
