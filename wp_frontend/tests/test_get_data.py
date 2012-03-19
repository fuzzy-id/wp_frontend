# -*- coding: utf-8 -*-
import datetime
import random
from wp_frontend.compat import unittest

from pyramid import testing

import wp_frontend
from wp_frontend.models import get_data
from wp_frontend.models.calculations import CurrKW
from wp_frontend import tests
from wp_frontend.tests import create_entries
from wp_frontend.views import wp_datetime

class PulledDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmp_session = tests.create_engine_and_init_db(db_reset=True)
        tmp_session.remove()

    def setUp(self):
        self.transaction = tests.getTransaction()
        self.session = tests.create_engine_and_init_db()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _add_one(self, *args):
        self.transaction.begin()
        entry = get_data.PulledData(*args)
        self.session.add(entry)
        self.transaction.commit()

    def test_default_values_are_setted(self):
        dt_before = wp_datetime.strip_ms(datetime.datetime.now())
        self._add_one({})
        dt_after = wp_datetime.strip_ms(datetime.datetime.now())
        cols = ['version', 'datum_version', 'betriebsmodus',
                'temp_aussen', 'tsp', ]
        entry = get_data.PulledData.get_latest(self.session, cols)
        self.assertEqual(entry[0], 0)
        self.assertEqual(entry[1], datetime.date.min)
        self.assertEqual(entry[2], '')
        self.assertEqual(entry[3], 0.0)
        entry_date = datetime.datetime.fromtimestamp(entry[4])
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

    @tests.reset_db
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

    def test_get_calculated_entries(self):
        entry = {'temp_Vl': 18.0,
                 'temp_Vl': 18.0,
                 'temp_Rl': 14.4,
                 'temp_WQein': 12.5,
                 'temp_WQaus': 10.0,
                 }
        self._add_one(entry)

        expected = 18.0 * 0.06 + 0.5
        result = get_data.PulledData.get_latest(self.session, ['currKW', ])
        self.assertEquals(result[0], expected)

        expected = 18.0 - 14.4
        result = get_data.PulledData.get_latest(self.session, ['deltaVlRl', ])
        self.assertEquals(result[0], expected)

        expected = 12.5 - 10.0
        result = get_data.PulledData.get_latest(self.session, ['deltaWQea', ])
        self.assertEquals(result[0], expected)

if __name__ == '__main__': unittest.main()
