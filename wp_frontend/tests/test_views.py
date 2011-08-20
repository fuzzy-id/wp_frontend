# -*- coding: utf-8 -*-
import datetime
import random
import unittest

from pyramid import testing

from wp_frontend import views
from wp_frontend.tests import getTransaction, createEngineAndInitDB
from wp_frontend.models import get_data


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

class BaseViewTest(unittest.TestCase):

    def setUp(self):
        self.transaction = getTransaction()
        self.session = createEngineAndInitDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _add_one(self, *args):
        self.transaction.begin()
        entry = self._class_to_add()(*args)
        self.session.add(entry)
        self.transaction.commit()

class ViewHomeTests(BaseViewTest):

    def _class_to_add(self):
        return get_data.PulledData

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

class ViewHzgWWTests(BaseViewTest):

    def _class_to_add(self):
        return get_data.PulledData

    def test_without_data_present(self):
        request = testing.DummyRequest()
        response = views.view_hzg_ww(request)
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
                                            'submit': 'submit', })
        request.params = request.get
        response = views.view_hzg_ww(request)

        self.assertTrue(response['vals_available'] == False)
        result = response['start'].strftime("%Y-%m-%d %H:%M:%S")
        self.assertEquals(result, start)
        result = response['end'].strftime("%Y-%m-%d %H:%M:%S")
        self.assertEquals(result, end)
        
    def test_invalid_date_format_gives_error_in_form(self):
        end = "2011-08-10 20"
        start = "2011-08-20 23:18:00"
        request = testing.DummyRequest(get={'start': start,
                                            'end': end,
                                            'submit': 'submit', })
        request.params = request.get
        response = views.view_hzg_ww(request)

        self.assertTrue(response['vals_available'] == False)
        self.assertTrue('Invalid date' in response['form'])

    def test_end_before_start_gives_error_in_form(self):
        end = "2011-08-10 20:18:00"
        start = "2011-08-20 23:18:00"
        request = testing.DummyRequest(get={'start': start,
                                            'end': end, })
        response = views.view_hzg_ww(request)

        self.assertTrue(response['vals_available'] == False)
        
        
