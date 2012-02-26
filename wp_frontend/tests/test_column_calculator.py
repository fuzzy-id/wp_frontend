# -*- coding: utf-8 -*-
import unittest

from wp_frontend.models.calculations import register_all_calculations
from wp_frontend.models.column_calculator import _flatten_list, ColumnCalculator


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
