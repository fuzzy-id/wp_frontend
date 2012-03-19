# -*- coding: utf-8 -*-
import unittest
import webtest

import wp_frontend
from wp_frontend import tests
from wp_frontend.tests import create_entries

class ViewTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmp_session = tests.createEngineAndInitDB()
        tmp_session.remove()

    def setUp(self):
        app = wp_frontend.main({}, 
                               sql_init_function=tests.init_db, 
                               **tests.settings)
        self.testapp = webtest.TestApp(app)
        self.testapp.put('/login', tests.valid_credentials, status=302)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def test_status_page_viewable(self):
        res = self.testapp.get('/status', status=200)
        self.assertIn('Status', res.body)
        self.assertIn('Allgemein', res.body)
        self.assertIn('Backup', res.body)
        self.assertIn('Uptime', res.body)

    def test_status_backup_page_viewable(self):
        res = self.testapp.get('/backup/new_template', status=200)
        self.assertIn('Status', res.body)
        self.assertIn('Allgemein', res.body)
        self.assertIn('Backup', res.body)
    
class PageWithDbEntriesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmp_session = tests.createEngineAndInitDB()
        create_entries.add_backup_templates(tests.getTransaction(),
                                            tmp_session)
        tmp_session.remove()

    def setUp(self):
        app = wp_frontend.main({}, 
                               sql_init_function=tests.init_db, 
                               **tests.settings)
        self.testapp = webtest.TestApp(app)
        self.testapp.put('/login', tests.valid_credentials, status=302)

    def tearDown(self):
        del self.testapp
        tests.getSession().remove()

    def test_sidebar_gets_updated(self):
        res = self.testapp.get('/status', status=200)
        self.assertIn('New Template', res.body)
        self.assertIn('Home', res.body)
        self.assertIn('System', res.body)
    
    def test_home_backup_page(self):
        res = self.testapp.get('/backup/home', status=200)
        self.assertIn('home', res.body)
        self.assertIn('/home', res.body)
