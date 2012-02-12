# -*- coding: utf-8 -*-

from wp_frontend.tests.test_functionals import BasicFunctionalTestCase

class AuthenticationTests(BasicFunctionalTestCase):

    def test_anonymous_cannot_view_status_page(self):
        res = self.testapp.get('/status', status=200)
        self.assertNotLoggedIn(res)

class ViewTests(BasicFunctionalTestCase):
    
    def test_status_page_viewable(self):
        res = self.testapp.get('/status', status=200)
        self.assertLoggedIn(res)
        self.assertIn(res.body, 'Status')
