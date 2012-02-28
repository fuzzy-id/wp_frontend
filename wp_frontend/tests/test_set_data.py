# -*- coding: utf-8 -*-
import datetime
import unittest

from wp_frontend.models import set_data
from wp_frontend import tests
from wp_frontend.views.wp_datetime import strip_ms


class DataToSetTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmp_session = tests.create_engine_and_init_db(db_reset=True)
        tmp_session.remove()

    def setUp(self):
        self.transaction = tests.getTransaction()
        self.session = tests.create_engine_and_init_db()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _add_one(self, *args):
        self.transaction.begin()
        entry = set_data.DataToSet(*args)
        self.session.add(entry)
        self.transaction.commit()
    
    def _get_last_entry(self):
        query = self.session.query(set_data.DataToSet)
        query = query.order_by(set_data.DataToSet.id.desc())
        return query.first()

    def test_db_empty_on_startup(self):
        query = self.session.query(set_data.DataToSet)
        entries = query.all()
        self.assertRaises(IndexError, entries.pop)

    def test_get_last_entry_works(self):
        self._add_one('test_user', 'Hzg:TempEinsatz', '23', '80')
        entry = self._get_last_entry()
        self.assertEquals(entry.newval, '23')
        self.assertEquals(entry.oldval, '80')
        self._add_one('test_user', 'Hzg:TempEinsatz', '24', '13.2')
        self._add_one('test_user', 'Hzg:TempEinsatz', '26', '12.3')
        entry = self._get_last_entry()
        self.assertEquals(entry.newval, '26')
        self.assertEquals(entry.oldval, '12.3')

    def test_datetime_of_entry(self):
        self._add_one('test_user', 'Hzg:TempEinsatz', '23', '32')
        dt_after = strip_ms(datetime.datetime.now())
        entry = self._get_last_entry()
        self.assertEquals(dt_after, entry.datetime)
