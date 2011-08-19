# -*- coding: utf-8 -*-
import unittest
from pyramid import testing
from wp_frontend import views
from wp_frontend.tests import getTransaction, createEngineAndInitDB

class RootViewTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_forward_via_view_home(self):
        request = testing.DummyRequest()
        self.config.add_route('view_home', '/home')
        response = views.view_wp(request)
        self.assertEqual(response.location, 'http://example.com/home')
        
class ViewHomeTests(unittest.TestCase):

    def setUp(self):
        self.session = createEngineAndInitDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_view_home_exists(self):
        request = testing.DummyRequest()
        response = views.view_home(request)
        self.assertTrue(response['data'] is None)
