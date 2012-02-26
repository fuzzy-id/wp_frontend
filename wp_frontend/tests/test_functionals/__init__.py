# -*- coding: utf-8 -*-
import unittest
import re

import wp_frontend
from webtest import TestApp
from wp_frontend import tests
from wp_frontend.tests import create_entries


valid_credentials = { 'user': 'test_user',
                      'password': 'password',
                      'came_from': '/',
                      'submit': '', }

class BasicFunctionalTestCase(unittest.TestCase):
    
    def setUp(self):
        app = wp_frontend.main(
            {}, 
            sql_init_function=tests.init_and_recreate_db, 
            **tests.settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def login(self):
        return self.testapp.put('/login', valid_credentials, status=302)

    def logout(self):
        return self.testapp.get('/logout')

    def assertLoggedIn(self, res):
        self.assertTrue('input type="password"' not in res.body)

    def assertNotLoggedIn(self, res):
        self.assertTrue('input type="password"' in res.body)
        

class BehaviourForAnonymousTests(unittest.TestCase):

    def setUp(self):
        app = wp_frontend.main({}, 
                               sql_init_function=tests.init_db, 
                               **tests.settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def test_root_forwards_to_home(self):
        res = self.testapp.get('/', status=302)
        self.assertEqual(res.location, 'http://localhost/home')

    def test_unexisting_page_gives_404(self):
        res = self.testapp.get('/InexistentPage', status=404)
        
    def test_anonymous_cannot_view(self):
        res = self.testapp.get('/home', status=200)
        self.assertTrue('input type="password"' in res.body)
        res = self.testapp.get('/graph/hzg_ww/', status=200)
        self.assertTrue('input type="password"' in res.body)
        res = self.testapp.get('/set_val', status=200)
        self.assertTrue('input type="password"' in res.body)

class AuthenticationTests(unittest.TestCase):

    def setUp(self):
        app = wp_frontend.main({}, 
                               sql_init_function=tests.init_db, 
                               **tests.settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def test_login_and_logout(self):
        self.testapp.put('/login', valid_credentials, status=302)
        res = self.testapp.get('/home')
        self.assertNotIn('input type="password"', res.body)
        self.testapp.get('/logout')
        res = self.testapp.get('/home')
        self.assertIn('input type="password"', res.body)
        
    def test_failed_log_in(self):
        invalid_credentials = { 'user': 'invalid_user',
                                'password': 'invalid_password',
                                'came_from': '/',
                                'submit': '', }
        res = self.testapp.put('/login', invalid_credentials, status=200)
        res = self.testapp.get('/home')
        self.assertIn('input type="password"', res.body)

    def test_garbage_log_in(self):
        garbage_credentials = {'foo': 'baz', 'submit': ''}
        res = self.testapp.put('/login', garbage_credentials,
                               status=200)
        self.assertIn('input type="password"', res.body)
        self.assertIn('There was a problem with your submission', res.body)
