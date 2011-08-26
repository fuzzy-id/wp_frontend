import datetime
import time
import random
import unittest

from wp_frontend.models import set_data, get_data
from wp_frontend.models.calculations import register_all_calculations, calc_currKW
from wp_frontend.models.column_calculator import _flatten_list, ColumnCalculator
from wp_frontend.tests import BaseTestWithDB, strip_ms
from wp_frontend.views import strip_min_ms

class DataToSetTest(BaseTestWithDB):

    def _make_the_class(self, *args):
        return set_data.DataToSet(*args)
    
    def _get_last_entry(self):
        query = self.session.query(set_data.DataToSet)
        query = query.order_by(set_data.DataToSet.id.desc())
        return query.first()

    def test_db_empty_on_startup(self):
        query = self.session.query(set_data.DataToSet)
        entries = query.all()
        self.assertRaises(IndexError, entries.pop)

    def test_get_last_entry_works(self):
        self._add_one('test_user', 'Hzg:TempEinsatz', '23', '80')
        entry = self._get_last_entry()
        self.assertEquals(entry.newval, '23')
        self.assertEquals(entry.oldval, '80')
        self._add_one('test_user', 'Hzg:TempEinsatz', '24', '13.2')
        self._add_one('test_user', 'Hzg:TempEinsatz', '26', '12.3')
        entry = self._get_last_entry()
        self.assertEquals(entry.newval, '26')
        self.assertEquals(entry.oldval, '12.3')

    def test_datetime_of_entry(self):
        self._add_one('test_user', 'Hzg:TempEinsatz', '23', '32')
        dt_after = strip_ms(datetime.datetime.now())
        entry = self._get_last_entry()
        self.assertEquals(dt_after, entry.datetime)

class PulledDataTest(BaseTestWithDB):

    def _make_the_class(self, *args):
        return get_data.PulledData(*args)

    def test_defaults_work(self):
        self._add_one({})
        columns = ['version', 'datum_version', 'betriebsmodus',
                   'temp_aussen']
        entry = get_data.PulledData.get_latest(self.session, columns)
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

    def test_avg_timespan_iterator(self):
        end = datetime.datetime.now()
        end = strip_min_ms(end)
        start = end - datetime.timedelta(days=80)
        quantity = 18
        expected_step = (end - start) / quantity
        current_start = start

        for (tsp_avg_start,
             tsp_avg_end) in get_data._avg_timespan_iter(start,
                                                         end,
                                                         quantity):
            dt_avg_start = datetime.datetime.fromtimestamp(tsp_avg_start)
            dt_avg_end = datetime.datetime.fromtimestamp(tsp_avg_end)
            self.assertEquals(dt_avg_start, current_start)
            current_start += expected_step
            self.assertEquals(dt_avg_end, current_start)

    def test_get_values_in_timespan_with_avg(self):
        start = datetime.datetime.min
        end = start + datetime.timedelta(days=30)
        quantity = 10

        expected = {}


        for avg_start, avg_end in get_data._avg_timespan_iter(start,
                                                              end,
                                                              quantity):
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
            self.session, ['tsp', 'temp_aussen', 'currKW'], start, end,
            quantity)

        self.assertEquals(number, quantity)
        
        for entry in entries:
            res_tsp = int(entry[0])
            self.assertTrue(res_tsp in expected)
            self.assertEquals(entry[1], expected[res_tsp][0])
            self.assertEquals(entry[2], expected[res_tsp][1])
        
    def test_get_values_in_timespan_wo_avg(self):
        start = datetime.datetime.min
        end = start + datetime.timedelta(days=10)
        tsp_start = int(time.mktime(start.timetuple()))
        tsp_end = int(time.mktime(end.timetuple()))
        quantity = 100

        step = (tsp_end - tsp_start) / quantity
        
        expected = {}

        for tsp in range(tsp_start, tsp_end, step):
            temp_aussen = random.randint(-10, 50)
            temp_Vl = random.randint(-10, 50)
                
            entry = {'tsp': tsp,
                     'temp_aussen': temp_aussen,
                     'temp_Vl': temp_Vl}

            self._add_one(entry)
                
            expected[tsp] = (temp_aussen,
                             calc_currKW(temp_Vl), )

        number, entries = get_data.PulledData.get_values_in_timespan(
            self.session, ['tsp', 'temp_aussen', 'currKW'], start, end,
            quantity*3)

        self.assertEquals(number, quantity)
        
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

class ColumnCalculatorTests(unittest.TestCase):

    def setUp(self):
        ColumnCalculator.available_calculations = {}

    def tearDown(self):
        register_all_calculations()

    def test_flatten_list(self):
        test_list = [8, [98, [0, 'raen']], ['gf'], 8]
        expected =  [8, 98, 0, 'raen', 'gf', 8]
        result = _flatten_list(test_list)
        self.assertEqual(result, expected)

    def test_add_entries(self):
        class DummyCalculation(object):
            name = 'dummy_calc'
            needed_columns = ['foo', 'bar']

        ColumnCalculator.register_calculation(DummyCalculation)

        cols = ['braz', 'uiae', 'dummy_calc', 'nrtd']
        cc = ColumnCalculator(cols)
        expected = ['braz', 'uiae', 'foo', 'bar', 'nrtd']
        result = cc.add_entries(cols)
        self.assertEqual(result, expected)

    def test_calculate_entries_without_registered_calculations(self):
        cols = ['braz', 'uiae', 'dummy_calc', 'nrtd']
        cc = ColumnCalculator(cols)
        entries = ('braz', 'uiae', 1, 'nrtd', )

        result = cc.add_entries(list(entries))
        self.assertEqual(tuple(result), entries)

        result = cc.calculate_entries(list(entries))
        self.assertEqual(result, entries)
        
    def test_calculate_entries(self):
        class DummyCalculation(object):
            name = 'dummy_calc'
            needed_columns = ['foo', 'bar']
            @staticmethod
            def calc(val1, val2):
                return val1 - val2
        
        ColumnCalculator.register_calculation(DummyCalculation)

        cols = ['braz', 'uiae', 'dummy_calc', 'nrtd']
        cc = ColumnCalculator(cols)
        entries = ['braz', 'uiae', 1, 5, 'nrtd']
        result = cc.calculate_entries(entries)
        expected = ('braz', 'uiae', -4, 'nrtd', )
        self.assertEqual(result, expected)
        
