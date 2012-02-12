# -*- coding: utf-8 -*-

from wp_frontend.tests.test_functionals import BasicFunctionalTestCase

class AuthenticationTests(BasicFunctionalTestCase):

    def test_anonymous_cannot_view_status_page(self):
        res = self.testapp.get('/status', status=200)
        self.assertNotLoggedIn(res)

    def test_anonymous_cannot_view_status_backup_page(self):
        res = self.testapp.get('/status/backup', status=200)
        self.assertNotLoggedIn(res)

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
        res = self.testapp.get('/status/backup', status=200)
        self.assertLoggedIn(res)
        self.assertIn('Status', res.body)
        self.assertIn('Allgemein', res.body)
        self.assertIn('Backup', res.body)
