import unittest2
import re

import wp_frontend
from webtest import TestApp
from wp_frontend import tests
from wp_frontend.tests import create_entries


valid_credentials = { 'user': 'test_user',
                      'password': 'password',
                      'came_from': '/',
                      'submit': '', }

class BasicFunctionalTestCase(unittest2.TestCase):
    
    def setUp(self):
        app = wp_frontend.main({}, sql_init_function=tests.init_testing_db, **tests.settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def login(self):
        return self.testapp.put('/login', valid_credentials,
                                status=302)
    def logout(self):
        return self.testapp.get('/logout')

    def assertLoggedIn(self, res):
        self.assertTrue('input type="password"' not in res.body)

    def assertNotLoggedIn(self, res):
        self.assertTrue('input type="password"' in res.body)
        

class BehaviourForAnonymousTests(BasicFunctionalTestCase):

    def test_root_forwards_to_home(self):
        res = self.testapp.get('/', status=302)
        self.assertEqual(res.location,
                         'http://localhost/home')

    def test_unexisting_page_gives_404(self):
        res = self.testapp.get('/InexistentPage', status=404)
        
    def test_anonymous_cannot_view(self):
        res = self.testapp.get('/home', status=200)
        self.assertNotLoggedIn(res)
        res = self.testapp.get('/graph/hzg_ww', status=200)
        self.assertNotLoggedIn(res)
        res = self.testapp.get('/set_val', status=200)
        self.assertNotLoggedIn(res)

class AuthenticationTests(BasicFunctionalTestCase):

    def test_succesfull_login(self):
        self.login()
        res = self.testapp.get('/home')
        self.assertLoggedIn(res)
        
    def test_login(self):
        self.login()
        res = self.testapp.get('/home')
        self.assertLoggedIn(res)
        self.logout()
        res = self.testapp.get('/home')
        self.assertNotLoggedIn(res)
        
    def test_failed_log_in(self):
        invalid_credentials = { 'user': 'invalid_user',
                                'password': 'invalid_password',
                                'came_from': '/',
                                'submit': '', }
        res = self.testapp.put('/login', invalid_credentials,
                               status=200)
        res = self.testapp.get('/home')
        self.assertNotLoggedIn(res)

    def test_garbage_log_in(self):
        garbage_credentials = {'foo': 'baz', 'submit': ''}
        res = self.testapp.put('/login', garbage_credentials,
                               status=200)
        self.assertNotLoggedIn(res)
        self.assertTrue('There was a problem with your submission' in res.body)

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
        create_entries.add_entries_to_db(tests.getTransaction(), tests.getSession())
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
