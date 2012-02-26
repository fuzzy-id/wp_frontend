# -*- coding: utf-8 -*-
from wp_frontend import tests
from wp_frontend.tests import create_entries
from wp_frontend.tests.test_functionals import BasicFunctionalTestCase

class ViewTests(BasicFunctionalTestCase):
    
    def setUp(self):
        super(ViewTests, self).setUp()
        self.login()

    def test_status_page_viewable(self):
        res = self.testapp.get('/status', status=200)
        self.assertLoggedIn(res)
        self.assertIn('Status', res.body)
        self.assertIn('Allgemein', res.body)
        self.assertIn('Backup', res.body)
        self.assertIn('Uptime', res.body)

    def test_status_backup_page_viewable(self):
        res = self.testapp.get('/backup/new_template', status=200)
        self.assertLoggedIn(res)
        self.assertIn('Status', res.body)
        self.assertIn('Allgemein', res.body)
        self.assertIn('Backup', res.body)

    
class PageWithDbEntriesTests(BasicFunctionalTestCase):

    def setUp(self):
        super(PageWithDbEntriesTests, self).setUp()
        create_entries.add_backup_templates(tests.getTransaction(),
                                            tests.getSession())
        self.login()

    def test_sidebar_gets_updated(self):
        res = self.testapp.get('/status', status=200)
        self.assertIn('New Template', res.body)
        self.assertIn('Home', res.body)
        self.assertIn('System', res.body)
    
    def test_home_backup_page(self):
        res = self.testapp.get('/backup/home', status=200)
        self.assertIn('home', res.body)
        self.assertIn('/home', res.body)
