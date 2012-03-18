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
        self.assertTrue('Status' in res.body)
        self.assertTrue('Allgemein' in res.body)
        self.assertTrue('Backup' in res.body)
        self.assertTrue('Uptime' in res.body)

    def test_status_backup_page_viewable(self):
        res = self.testapp.get('/backup/new_template', status=200)
        self.assertTrue('Status' in res.body)
        self.assertTrue('Allgemein' in res.body)
        self.assertTrue('Backup' in res.body)
    
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
        self.assertTrue('New Template' in res.body)
        self.assertTrue('Home' in res.body)
        self.assertTrue('System' in res.body)
    
    def test_home_backup_page(self):
        res = self.testapp.get('/backup/home', status=200)
        self.assertTrue('home' in res.body)
        self.assertTrue('/home' in res.body)
