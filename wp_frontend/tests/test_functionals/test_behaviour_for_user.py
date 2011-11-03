# -*- coding: utf-8 -*-
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
        self.assertTrue("Couldn't get any data!" in res.body)

    def test_view_set_val(self):
        res = self.testapp.get('/set_val')
        self.assertTrue("Couldn't fetch logs." in res.body)
        self.assertTrue("Couldn't fetch current values." in res.body)

    def _test_view_graph(self, path_to_graph):
        res = self.testapp.get(path_to_graph)
        self.assertTrue("Couldn't fetch any data to plot." in res.body)

    def test_view_graph_hzg_ww(self):
        self._test_view_graph('/graph/hzg_ww')

    def test_view_graph_erdsonde(self):
        self._test_view_graph('/graph/erdsonde')

    def test_view_graph_vorl_kondens(self):
        self._test_view_graph('/graph/vorl_kondens')

    def test_view_graph_wqaus_verdamp(self):
        self._test_view_graph('/graph/wqaus_verdamp')


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
        self.assertTrue("Plotted from 2011-10-14 18:00:00 to 2011-10-24 18:00:00 with 10 dots." 
                        in res.body)
        match = re.search(r'<img id="diag" src="(.*\.svgz)" />', res.body)
        return match.groups()[0]

    def test_plot_hzg_ww(self):
        self._get_plot('/graph/hzg_ww')

    def test_plot_erdsonde(self):
        self._get_plot('/graph/erdsonde')

    def test_plot_vorl_kondens(self):
        self._get_plot('/graph/vorl_kondens')

    def test_plot_wqaus_verdamp(self):
        self._get_plot('/graph/wqaus_verdamp')

    def test_field_defaults_are_not_empty(self):
        resp = self.testapp.get('/graph/erdsonde')
        self.assertNotIn('value=""', resp.body)
