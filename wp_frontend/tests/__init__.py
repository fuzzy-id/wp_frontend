# -*- coding: utf-8 -*-
import tempfile
import unittest

import transaction
from pyramid import testing
from sqlalchemy import create_engine
from wp_frontend.models import DBSession, Base, initialize_sql
from wp_frontend import settings
import wp_frontend

settings.plots_dir = tempfile.mkdtemp()

sql_url = 'mysql://test_user:D3v3L0p3R@localhost/testing'

settings = {'sqlalchemy.url': sql_url, }

class BaseTestWithDB(unittest.TestCase):

    def setUp(self):
        self.transaction = getTransaction()
        self.session = createEngineAndInitDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _add_one(self, *args):
        self.transaction.begin()
        entry = self._make_the_class(*args)            
        self.session.add(entry)
        self.transaction.commit()

def createEngineAndInitDB(sql_url=sql_url,
                          sql_echo=False):
    engine = create_engine(sql_url, echo=sql_echo)
    return init_testing_db(engine)

def init_testing_db(engine):
    initialize_sql(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return DBSession

def getSession():
    return DBSession

def getTransaction():
    return transaction
