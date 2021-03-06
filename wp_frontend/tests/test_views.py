# -*- coding: utf-8 -*-
import datetime
import os.path
import random
from wp_frontend.compat import unittest

import wp_frontend.views.graphs
from pyramid import testing
from wp_frontend import views
from wp_frontend import tests
from wp_frontend.tests import create_entries
from wp_frontend.models import calculations
from wp_frontend.models import get_data, helpers
from wp_frontend.views import wp_datetime, set_val

class RootViewTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_forward_via_view_home(self):
        request = testing.DummyRequest()
        self.config.add_route('view_home', '/home')
        response = views.view_wp(request)
        self.assertEqual(response.location, '/home')

class ViewHomeTests(unittest.TestCase):

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

    @tests.reset_db
    def test_view_home_without_data(self):
        request = testing.DummyRequest()
        response = views.view_home(request)
        self.assertFalse(response['current_data'].data_available)

    def test_view_home_with_data(self):
        now = datetime.datetime.now()
        one_year_ago = datetime.datetime(now.year, now.month-1, now.day,
                                         now.hour, now.minute, now.second)
        data_now = {'tsp': wp_datetime.convert_to_timestamp(now),
                    'version':8L,
                    'datum_version': datetime.date.today(),
                    'betriebsmodus': 'test',
                    'uhrzeit': datetime.time(21, 32, 8),
                    'datum': datetime.date.today(),
                    'DO_buffer': 'foo',
                    'DI_buffer': 'bar' }
        data_one_year_ago = {'tsp': wp_datetime.convert_to_timestamp(one_year_ago),
                             'betriebsmodus': 'test', }
        float_columns = ['temp_aussen', 'temp_aussen24', 'temp_aussen1',
                         'temp_RlSoll', 'temp_Rl', 'temp_Vl', 'ww_TempSoll',
                         'ww_TempIst', 'temp_raum', 'temp_raum1', 'temp_WQein',
                         'temp_WQaus', 'temp_Verdampfer', 'temp_Kondensator',
                         'temp_Saugleitung', 'druck_Verdampfer',
                         'druck_Kondensator', 'betr_h_hzg_pu', 'betr_h_ww_pu' ]
        for col in float_columns:
            data_now[col] = float(random.randint(-30, 70))
            data_one_year_ago[col] = random.randint(-30, 70)

        self._add_one(data_one_year_ago)
        self._add_one(data_now)

        data_now['currKW'] = calculations.CurrKW.calc(data_now['temp_Vl'])
        data_now['deltaVlRl'] = data_now['temp_Vl'] - data_now['temp_Rl']
        data_now['deltaWQea'] = data_now['temp_WQein'] - data_now['temp_WQaus']
        data_now['betrHWwPlusHzg'] = (
            (data_now['betr_h_ww_pu'] - data_one_year_ago['betr_h_ww_pu'])
            + (data_now['betr_h_hzg_pu'] - data_one_year_ago['betr_h_hzg_pu']))
        data_now['verbrauch'] = data_now['betrHWwPlusHzg'] * 1.9177
        del data_now['tsp']
        del data_now['betr_h_ww_pu']
        del data_now['betr_h_hzg_pu']

        request = testing.DummyRequest()
        response = views.view_home(request)
        result = dict([ (field, getattr(response['current_data'], field)) 
                        for field in data_now ])
        self.maxDiff = None
        self.assertDictEqual(result, data_now)

class ViewSetValTests(unittest.TestCase):

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

    @tests.reset_db
    def test_view_without_data_present(self):

        request = testing.DummyRequest()
        response = set_val.view_set_val(request)

        self.assertFalse(response['current_data'].data_available)
        self.assertTrue(response['log'] is None)
        self.assertTrue(response['form'] is not None)

    def test_view_with_log(self):
        
        create_entries.add_set_data_entries_to_db(self.transaction, self.session)

        expected = [ tuple([row[4], row[0], row[1], row[3], row[2], 'pending', '', ])
                     for row in create_entries.set_data_entries]
        expected.reverse()

        request = testing.DummyRequest()
        response = set_val.view_set_val(request)

        self.assertFalse(response['current_data'].data_available)
        for actual, exp in zip(response['log'], expected):
            self.assertEqual(actual, exp)

    def test_submit_works(self):

        attribute = 'temp_einsatz'
        newval = '22.7'
        request = testing.DummyRequest(params={'attr': attribute,
                                               'newval':newval,
                                               'submit': 'submit', })

        oldval = None
        user = None
        attribute = helpers.map_to_beautifull_names[attribute]
                                       
        expected = ("don't compare datetime", user, attribute,
                    oldval, str(newval), 'pending', '', )
        dt_before = wp_datetime.strip_ms(datetime.datetime.now())
        response = set_val.view_set_val(request)
        dt_after = wp_datetime.strip_ms(datetime.datetime.now())
        
        self.assertFalse(response['current_data'].data_available)
        self.assertTrue(response['log'][0][0] >= dt_before)
        self.assertTrue(dt_after >= response['log'][0][0])
        self.assertEqual(response['log'][0][1:-1], expected[1:-1])
        
    def test_submit_garbage_gives_error(self):
        request = testing.DummyRequest(params={'invalid_attr': 'invalid_value',
                                               'submit': ''})

        response = set_val.view_set_val(request)
        self.assertTrue('There was a problem with your submission' 
                        in response['form'])
        

class PlotsTests(unittest.TestCase):

    def test_create_empty_plot(self):
        plot = views.plots.make_plot([], [])
        self.assertTrue(os.path.isfile(plot))

    def test_get_plot_works(self):
        plot = views.plots.make_plot([], [])
        fname = os.path.basename(plot)
        request = testing.DummyRequest()
        request.matchdict['img_name'] = fname
        response = views.plots.get_plot(request)
        orig_img = open(plot)
        expected = ''.join(orig_img.readlines())
        self.assertEqual(expected, response.body)

    
