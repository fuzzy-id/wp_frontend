import unittest

from webtest import TestApp

import wp_frontend
from wp_frontend.models import DBSession
from wp_frontend.tests import init_testing_db, sql_url

settings = {'sqlalchemy.url': sql_url}

user_wrong_login = ('/login?login=inexistent_user'
                    + '&password=incorrect'
                    + '&came_from=home'
                    + '&form.submitted=Login')
    
class BaseTests(unittest.TestCase):

    def setUp(self):
        app = wp_frontend.main({}, sql_init_function=init_testing_db, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp
        DBSession.remove()

    def test_root_forwards_to_home(self):
        res = self.testapp.get('/', status=302)
        self.assertEqual(res.location,
                         'http://localhost/home')

    def test_unexisting_page_gives_404(self):
        res = self.testapp.get('/InexistentPage', status=404)
        
    def test_failed_log_in(self):
        res = self.testapp.get(user_wrong_login,
                               status=200)
        self.assertTrue('input type="password"' in res.body)

class AuthenticationTests(unittest.TestCase):

    def setUp(self):
        app = wp_frontend.main({}, sql_init_function=init_testing_db, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp
        DBSession.remove()

    def test_anonymous_cannot_view(self):
        res = self.testapp.get('/home', status=200)
        self.assertTrue('input type="password"' in res.body)
        res = self.testapp.get('/graph/hzg_ww', status=200)
        self.assertTrue('input type="password"' in res.body)
        res = self.testapp.get('/set_val', status=200)
        self.assertTrue('input type="password"' in res.body)
