# -*- coding: utf-8 -*-
import os.path
import tempfile
import unittest

import transaction
from pyramid import testing
from sqlalchemy import create_engine
from wp_frontend.models import DBSession, Base, initialize_sql
from wp_frontend import settings
import wp_frontend

settings.plots_dir = tempfile.mkdtemp()

sql_url = 'sqlite://'

here = os.path.abspath(os.path.dirname(__file__))

settings = {'sqlalchemy.url': sql_url, 
            'credentials': os.path.join(here, 'passwd.py'),
            }

valid_credentials = { 'user': 'test_user',
                      'password': 'password',
                      'came_from': '/',
                      'submit': '', }

import functools

def reset_db(f):
    @functools.wraps(f)
    def db_resetter(inst):
        inst.session.remove()
        inst.session = create_engine_and_init_db(db_reset=True)
        return f(inst)
    return db_resetter
        
def createEngineAndInitDB(sql_url=sql_url,
                          sql_echo=False):
    engine = create_engine(sql_url, echo=sql_echo)
    return init_and_recreate_db(engine)

def create_engine_and_init_db(db_reset=False,
                              sql_url=sql_url,
                              sql_echo=False):
    engine = create_engine(sql_url, echo=sql_echo)
    if db_reset:
        return init_and_recreate_db(engine)
    return init_db(engine)

def init_db(engine):
    initialize_sql(engine)
    return DBSession

def init_and_recreate_db(engine):
    initialize_sql(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return DBSession

def getSession():
    return DBSession

def getTransaction():
    return transaction
