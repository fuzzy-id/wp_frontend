# -*- coding: utf-8 -*-
import pprint
import re
from wp_frontend import tests
from wp_frontend.tests import create_entries
from wp_frontend.tests.test_functionals import BasicFunctionalTestCase


class BehaviourForUserWithoutDBTests(BasicFunctionalTestCase):

    def setUp(self):
        BehaviourForUserWithoutDBTests.__base__.setUp(self)
        self.login()

    def test_view_home(self):
        res = self.testapp.get('/home')
        self.assertIn("Couldn't get any data", res.body)

    def test_view_set_val(self):
        res = self.testapp.get('/set_val')
        self.assertIn("Couldn't fetch logs", res.body)
        self.assertIn("Couldn't fetch current values", res.body)

    def _test_view_graph(self, path_to_graph):
        res = self.testapp.get(path_to_graph)
        self.assertIn("Couldn't fetch any data to plot", res.body)

    def test_view_graph_hzg_ww(self):
        self._test_view_graph('/graph/hzg_ww/')

    def test_view_graph_erdsonde(self):
        self._test_view_graph('/graph/erdsonde/')

    def test_view_graph_vorl_kondens(self):
        self._test_view_graph('/graph/vorl_kondens/')

    def test_view_graph_wqaus_verdamp(self):
        self._test_view_graph('/graph/wqaus_verdamp/')

    def test_view_user_graph(self):
        self._test_view_graph('/graph/user/temp_Vl/temp_Rl')
        
    def test_form_on_user_graph_page_exists(self):
        res = self.testapp.get('/user_graph')
        self.assertIn('temp_Vl', res.body)

    def test_error_in_form_submission_is_properly_handled(self):
        attributes = [('foo', 'bar'), ('submit', 'submit')]
        resp = self.testapp.post('/user_graph', attributes)
        self.assertIn('There was a problem with your submission', resp.body)

    def test_wrong_attributes_result_in_form_error(self):
        attributes = [('__start__', 'attr_list:sequence'), 
                      ('checkbox', 'not_existing_attribute'), 
                      ('__end__', 'attr_list:sequence'), 
                      ('submit', 'submit')]
        resp = self.testapp.post('/user_graph', attributes)
        self.assertIn("Unknown attribute: 'not_existing_attribute'", resp.body)

    def test_user_graph_forwards_properly_to_graph_page(self):
        attributes = [('__start__', 'attr_list:sequence'), 
                      ('checkbox', 'ww_TempSoll'), 
                      ('checkbox', 'deltaVlRl'), 
                      ('__end__', 'attr_list:sequence'), 
                      ('submit', 'submit')]
        resp = self.testapp.post('/user_graph', attributes, status=302)
        self.assertIn('/graph/user/ww_TempSoll/deltaVlRl', resp.body)

    def test_invalid_attr_is_properly_handled_on_graph_user(self):
        resp = self.testapp.get('/graph/user/foo', status=400)
        self.assertIn("Attribute '%s' is not plotable.", resp.body)

class BehaviourForUserWithDBTests(BasicFunctionalTestCase):

    timespan = {'start': "2011-10-14 18:00:00",
                'end': "2011-10-24 18:00:00",
                'resolution': '10',
                'submit': 'submit'}

    def setUp(self):
        BehaviourForUserWithDBTests.__base__.setUp(self)
        create_entries.add_get_data_entries_to_db(tests.getTransaction(), 
                                                  tests.getSession())
        self.login()

    def test_view_home(self):
        res = self.testapp.get('/home')
        self.assertTrue('2011-10-24' in res.body)
        self.assertTrue('18:00:00' in res.body)

    def _get_plot(self, path_to_plot):
        res = self.testapp.post(path_to_plot, self.timespan)
        self.assertIn("2011-10-14 18:00:00", res.body)
        self.assertIn("2011-10-24 18:00:00", res.body)
        self.assertIn("10", res.body)
        match = re.search(r'<img src="(.*\.svgz)" />', res.body)
        return match.groups()[0]

    def test_plot_hzg_ww(self):
        self._get_plot('/graph/hzg_ww/')

    def test_plot_erdsonde(self):
        self._get_plot('/graph/erdsonde/')

    def test_plot_vorl_kondens(self):
        self._get_plot('/graph/vorl_kondens/')

    def test_plot_wqaus_verdamp(self):
        self._get_plot('/graph/wqaus_verdamp/')

class GraphFormTests(BasicFunctionalTestCase):

    def setUp(self):
        BehaviourForUserWithoutDBTests.__base__.setUp(self)
        self.login()

    def test_field_defaults_are_setted(self):
        resp = self.testapp.get('/graph/erdsonde/')
        self.assertNotIn('value=""', resp.body)

    def test_error_goes_away_when_requesting_other_page(self):
        wrong_tsp = { 'start': "2011-10-24 18:00:00",
                      'end': "2011-10-14 18:00:00",
                      'resolution': '10',
                      'submit': 'submit'}
        resp = self.testapp.post('/graph/erdsonde/', wrong_tsp)
        self.assertIn('There was a problem with your submission', resp.body)
        resp = self.testapp.get('/graph/hzg_ww/')
        self.assertNotIn('There was a problem with your submission', resp.body)
