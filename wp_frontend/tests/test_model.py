import datetime
import unittest
from wp_frontend.tests import getTransaction, createEngineAndInitDB
from wp_frontend.models import set_data 
from wp_frontend.models import get_data 

class DataToSetTest(unittest.TestCase):
    
    def setUp(self):
        self.transaction = getTransaction()
        self.session = createEngineAndInitDB()

    def tearDown(self):
        self.session.remove()

    def _add_one(self, user, attribute, newval):
        self.transaction.begin()
        entry = set_data.DataToSet(user, attribute, newval)
        self.session.add(entry)
        self.transaction.commit()
        return entry

    def _get_last_entry(self):
        query = self.session.query(set_data.DataToSet)
        query = query.order_by(set_data.DataToSet.id.desc())
        return query.first()

    def test_db_empty_on_startup(self):
        query = self.session.query(set_data.DataToSet)
        entries = query.all()
        self.assertRaises(IndexError, entries.pop)

    def test_get_last_entry_works(self):
        self._add_one('test_user', 'Hzg:TempEinsatz', '23')
        entry = self._get_last_entry()
        self.assertEquals(entry.newval, '23')
        self._add_one('test_user', 'Hzg:TempEinsatz', '24')
        self._add_one('test_user', 'Hzg:TempEinsatz', '25')
        self._add_one('test_user', 'Hzg:TempEinsatz', '26')
        entry = self._get_last_entry()
        self.assertEquals(entry.newval, '26')
        self._add_one('test_user', 'Hzg:TempEinsatz', '27')
        self._add_one('test_user', 'Hzg:TempEinsatz', '28')
        entry = self._get_last_entry()
        self.assertEquals(entry.newval, '28')

    def test_datetime_of_entry(self):
        dt_before = datetime.datetime.now()
        self._add_one('test_user', 'Hzg:TempEinsatz', '23')
        dt_after = datetime.datetime.now()
        entry = self._get_last_entry()
        one_sec = datetime.timedelta(seconds=1)
        self.assertTrue(one_sec >= entry.datetime-dt_before)
        self.assertTrue(one_sec >= dt_after-entry.datetime)

class PulledDataTest(unittest.TestCase):

    def setUp(self):
        self.transaction = getTransaction()
        self.session = createEngineAndInitDB()

    def tearDown(self):
        self.session.remove()

    def _add_one(self, columns_and_values):
        self.transaction.begin()
        entry = get_data.PulledData(columns_and_values)
        self.session.add(entry)
        self.transaction.commit()

    def _get_last_entry(self):
        query = self.session.query(get_data.PulledData)
        query = query.order_by(get_data.PulledData.id.desc())
        return query.first()

    def test_defaults_work(self):
        self._add_one({})
        entry = self._get_last_entry()
        self.assertEqual(entry.version, 0)
        self.assertEqual(entry.datum_version, datetime.date.min)
        self.assertEqual(entry.betriebsmodus, '')
        self.assertEqual(entry.temp_aussen, 0.0)

    def test_add_one_and_get_last_entry_work(self):
        columns_and_values = {'temp_aussen': 24,
                              'temp_WW': 80.34 }
        self._add_one(columns_and_values)
        entry = self._get_last_entry()
        self.assertEqual(entry.temp_aussen, 24)
        self.assertEqual(entry.temp_WW, 80.34)

    def test_datetime_of_entry(self):
        dt_before = datetime.datetime.now()
        self._add_one({})
        dt_after = datetime.datetime.now()
        entry = self._get_last_entry()
        one_sec = datetime.timedelta(seconds=1)
        entry_date = datetime.datetime.fromtimestamp(entry.tsp)
        self.assertTrue(one_sec >= entry_date - dt_before)
        self.assertTrue(one_sec >= dt_after - entry_date)


