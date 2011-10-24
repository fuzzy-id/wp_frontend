# -*- coding: utf-8 -*-
import datetime
from wp_frontend.models import set_data
from wp_frontend.tests import BaseTestWithDB, strip_ms


class DataToSetTest(BaseTestWithDB):

    def _make_the_class(self, *args):
        return set_data.DataToSet(*args)
    
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
