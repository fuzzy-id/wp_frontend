# -*- coding: utf-8 -*-
import datetime
import random
import unittest

from pyramid import testing

from wp_frontend import views, tests
from wp_frontend.models import get_data, map_to_beautifull_names
from wp_frontend.models.set_data import DataToSet
from wp_frontend.tests import BaseTestWithDB
import wp_frontend.views.graphs


class RootViewTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_forward_via_view_home(self):
        request = testing.DummyRequest()
        self.config.add_route('view_home', '/home')
        response = views.view_wp(request)
        self.assertEqual(response.location, 'http://example.com/home')

class ViewHomeTests(BaseTestWithDB):

    def _make_the_class(self, *args):
        return get_data.PulledData(*args)

    def test_view_home_without_data(self):
        request = testing.DummyRequest()
        response = views.view_home(request)
        self.assertTrue(response['data'] is None)

    def test_view_home_with_data(self):
        data = {'version':8,
                'datum_version': datetime.date.today(),
                'betriebsmodus': 'test',
                'uhrzeit': datetime.time(21, 32, 8),
                'datum': datetime.date.today(),
                'DO_buffer': 'foo',
                'DI_buffer': 'bar' }
        float_columns = ['temp_aussen', 'temp_aussen24', 'temp_aussen1',
                         'temp_RlSoll', 'temp_Rl', 'temp_Vl', 'temp_WWSoll',
                         'temp_WW', 'temp_raum', 'temp_raum1', 'temp_WQein',
                         'temp_WQaus', 'temp_Verdampfer', 'temp_Kondensator',
                         'temp_Saugleitung', 'druck_Verdampfer',
                         'druck_Kondensator', 'betriebsstunden' ]
        for col in float_columns:
            data[col] = random.randint(-30, 70)

        self._add_one(data)

        request = testing.DummyRequest()
        response = views.view_home(request)
        result = response['data']

        from wp_frontend.models.calculations import calc_currKW
        data['currKW'] = calc_currKW(data['temp_Vl'])
        data['deltaVlRl'] = data['temp_Vl'] - data['temp_Rl']
        data['deltaWQea'] = data['temp_WQein'] - data['temp_WQaus']

        expected = data
        self.assertEqual(result, expected)

class ViewHzgWWTests(BaseTestWithDB):

    def _make_the_class(self, *args):
        return get_data.PulledData(*args)

    def test_without_data_present(self):
        request = testing.DummyRequest()
        request.matchdict['graph_name'] = 'hzg_ww'
        response = wp_frontend.views.graphs.view_graph(request)
        now = datetime.datetime.now()
        thirty_days_ago = now - datetime.timedelta(days=30)
        two_minutes = datetime.timedelta(minutes=2)
        self.assertTrue(response['vals_available'] == False)
        self.assertTrue(two_minutes >= now - response['end'])
        self.assertTrue(two_minutes >= thirty_days_ago - response['start'])

    def test_without_data_with_submitted_date(self):
        end = "2011-08-20 23:18:00"
        start = "2011-08-10 20:18:00"
        request = testing.DummyRequest(get={'start': start,
                                            'end': end,
                                            'resolution': '30',
                                            'submit': 'submit', })
        request.matchdict['graph_name'] = 'hzg_ww'
        request.params = request.get
        response = wp_frontend.views.graphs.view_graph(request)

        self.assertTrue(response['vals_available'] == False)
        result = response['start'].strftime("%Y-%m-%d %H:%M:%S")
        self.assertEquals(result, start)
        result = response['end'].strftime("%Y-%m-%d %H:%M:%S")
        self.assertEquals(result, end)
        
    def test_invalid_date_format_gives_error_in_form(self):
        start = "2011-08-10 20"
        end = "2011-08-20 23:18:00"
        request = testing.DummyRequest(get={'start': start,
                                            'end': end,
                                            'submit': 'submit', })
        request.matchdict['graph_name'] = 'hzg_ww'
        request.params = request.get
        response = wp_frontend.views.graphs.view_graph(request)

        self.assertTrue(response['vals_available'] == False)
        self.assertTrue('Invalid date' in response['form'])

    def test_end_before_start_gives_error_in_form(self):
        end = "2011-08-10 20:18:00"
        start = "2011-08-20 23:18:00"
        request = testing.DummyRequest(get={'start': start,
                                            'end': end,
                                            'resolution': '30',
                                            'submit': 'submit', })
        request.matchdict['graph_name'] = 'hzg_ww'
        request.params = request.get
        response = wp_frontend.views.graphs.view_graph(request)

        self.assertTrue(response['vals_available'] == False)
        self.assertTrue('Start has to be before End' in response['form'])
        

class ViewSetValTests(BaseTestWithDB):

    def _make_the_class(self, args):
        return DataToSet(*args)

    def test_view_without_data_present(self):

        request = testing.DummyRequest()
        response = views.view_set_val(request)

        self.assertTrue(response['current_values'] is None)
        self.assertTrue(response['log'] is None)
        self.assertTrue(response['form'] is not None)

    def test_view_with_log(self):
        
        user = 'test_user'
        attribute = 'Hzg:TempEinsatz'
        expected = []

        for i in range(10):
            newval = random.randint(-30, 70)
            oldval = random.randint(-30, 70)
            entry = (user, attribute, newval, oldval, )
            self._add_one(entry)
            expected.append((tests.strip_ms(datetime.datetime.now()),
                             user, attribute, str(oldval), str(newval),
                             'pending', '', ))

        expected.reverse()
        request = testing.DummyRequest()
        response = views.view_set_val(request)

        self.assertTrue(response['current_values'] is None)
        self.assertEqual(response['log'], expected)

    def test_submit_works(self):

        attribute = 'temp_einsatz'
        newval = '22.7'
        request = testing.DummyRequest(params={'attr': attribute,
                                               'newval':newval,
                                               'submit': 'submit', })

        oldval = None
        user = None
        attribute = map_to_beautifull_names[attribute]
                                       
        expected = (tests.strip_ms(datetime.datetime.now()), user, attribute,
                    oldval, str(newval), 'pending', '', )

        response = views.view_set_val(request)

        self.assertTrue(response['current_values'] is None)
        self.assertEqual(response['log'][0], expected)
        

