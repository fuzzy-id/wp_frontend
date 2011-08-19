# -*- coding: utf-8 -*-
import transaction
from sqlalchemy import create_engine

from wp_frontend.models import DBSession, Base, initialize_sql


sql_url = 'mysql://devel:D3v3L0p3R@localhost/wp_devel'

def createEngineAndInitDB(sql_url=sql_url,
                          sql_echo=False):
    engine = create_engine(sql_url, echo=sql_echo)
    return init_testing_db(engine)

def init_testing_db(engine):
    initialize_sql(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return DBSession

def getTransaction():
    return transaction
