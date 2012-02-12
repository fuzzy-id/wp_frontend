# -*- coding: utf-8 -*-

import unittest

class BasicStatusPageTests(unittest.TestCase):

    def test_view_status_page(self):

        res = self.testapp.get('/status')
