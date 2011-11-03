# -*- coding: utf-8 -*-

from wp_frontend import tests
from wp_frontend.tests import create_entries
from webtest import TestApp
import wp_frontend

tests.createEngineAndInitDB()

def make_testapp():
    app = wp_frontend.main({}, 
                           sql_init_function=tests.init_testing_db, 
                           **tests.settings)
    return TestApp(app)

def create_all_entries():
    create_entries.add_get_data_entries_to_db(
        tests.getTransaction(), tests.getSession())
    create_entries.add_set_data_entries_to_db(
        tests.getTransaction(), tests.getSession())
