# -*- coding: utf-8 -*-

from wp_frontend import tests
from wp_frontend.tests import create_entries

tests.createEngineAndInitDB()

def create_all_entries():
    create_entries.add_get_data_entries_to_db(
        tests.getTransaction(), tests.getSession())
    create_entries.add_set_data_entries_to_db(
        tests.getTransaction(), tests.getSession())
