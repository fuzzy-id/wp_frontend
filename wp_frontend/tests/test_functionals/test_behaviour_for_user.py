# -*- coding: utf-8 -*-
import re
from wp_frontend.compat import unittest

import webtest

import wp_frontend
from wp_frontend import tests
from wp_frontend.tests import create_entries

class BehaviourForUserWithoutDBTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmp_session = tests.createEngineAndInitDB()
        tmp_session.remove()

    def setUp(self):
        app = wp_frontend.main(
            {}, 
            sql_init_function=tests.init_db, 
            **tests.settings)
        self.testapp = webtest.TestApp(app)
        self.testapp.put('/login', tests.valid_credentials, status=302)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def test_view_home(self):
        res = self.testapp.get('/home')
        self.assertIn("Couldn't get any data", res.body)

    def test_view_set_val(self):
        res = self.testapp.get('/set_val')
        self.assertIn("Couldn't fetch logs", res.body)
        self.assertIn("Couldn't fetch current values", res.body)

    def test_view_graphs_wo_db_data(self):
        res = self.testapp.get('/graph/hzg_ww/')
        self.assertIn("Couldn't fetch any data to plot", res.body)

        res = self.testapp.get('/graph/erdsonde/')
        self.assertIn("Couldn't fetch any data to plot", res.body)

        res = self.testapp.get('/graph/vorl_kondens/')
        self.assertIn("Couldn't fetch any data to plot", res.body)

        res = self.testapp.get('/graph/wqaus_verdamp/')
        self.assertIn("Couldn't fetch any data to plot", res.body)

        res = self.testapp.get('/graph/user/temp_Vl/temp_Rl')
        self.assertIn("Couldn't fetch any data to plot", res.body)
        
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

    def test_resources_are_expanded(self):
        resp = self.testapp.get('/backup/new_template')
        self.assertIn('deform_static/css/form.css', resp.body)
        self.assertIn('deform_static/scripts/deform.js', resp.body)

        resp = self.testapp.get('/graph/erdsonde/')
        self.assertIn('deform_static/css/form.css', resp.body)
        self.assertIn('deform_static/scripts/deform.js', resp.body)

        resp = self.testapp.get('/graph/erdsonde/')
        self.assertIn('deform_static/css/form.css', resp.body)
        self.assertIn('deform_static/scripts/deform.js', resp.body)

class BehaviourForUserWithDBTests(unittest.TestCase):

    timespan = {'start': "2011-10-14 18:00:00",
                'end': "2011-10-24 18:00:00",
                'resolution': '10',
                'submit': 'submit'}

    @classmethod
    def setUpClass(cls):
        tmp_session = tests.createEngineAndInitDB()
        create_entries.add_get_data_entries_to_db(tests.getTransaction(), 
                                                  tmp_session)

        tmp_session.remove()

    def setUp(self):
        app = wp_frontend.main(
            {}, sql_init_function=tests.init_db, **tests.settings)
        self.testapp = webtest.TestApp(app)
        self.testapp.put('/login', tests.valid_credentials, status=302)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def test_view_home(self):
        res = self.testapp.get('/home')
        self.assertIn('2011-10-24', res.body)
        self.assertIn('18:00:00', res.body)

    def test_plot_hzg_ww(self):
        self._verify_plot('/graph/hzg_ww/')
        self._verify_plot('/graph/erdsonde/')
        self._verify_plot('/graph/vorl_kondens/')
        self._verify_plot('/graph/wqaus_verdamp/')

    def _verify_plot(self, path_to_plot):
        res = self.testapp.post(path_to_plot, self.timespan)
        self.assertIn("2011-10-14 18:00:00", res.body)
        self.assertIn("2011-10-24 18:00:00", res.body)
        self.assertIn("10", res.body)
        match = re.search(r'<img src="(.*\.svgz)" />', res.body)
        self.assertIsNot(match.groups()[0], None)

class GraphFormTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmp_session = tests.createEngineAndInitDB()
        create_entries.add_get_data_entries_to_db(tests.getTransaction(), 
                                                  tmp_session)
        tmp_session.remove()

    def setUp(self):
        app = wp_frontend.main(
            {}, sql_init_function=tests.init_db, **tests.settings)
        self.testapp = webtest.TestApp(app)
        self.testapp.put('/login', tests.valid_credentials, status=302)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

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
