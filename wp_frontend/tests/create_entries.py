# -*- coding: utf-8 -*-

import datetime
from wp_frontend.models.get_data import PulledData
from wp_frontend.models.set_data import DataToSet

# These get_data_entries start on 14/10/2011 18:00:00 and end on 24/10/2011 18:00:00 with
# five get_data_entries per day. That makes 50 get_data_entries...

entries_start = datetime.datetime(2011, 10, 14, 18)
entries_end = datetime.datetime(2011, 10, 24, 18)

get_data_entries = [
    {'tsp': 1318616640, 'temp_aussen': 10, 'temp_Vl': -10,},
    {'tsp': 1318633920, 'temp_aussen': 11, 'temp_Vl': -9, },
    {'tsp': 1318651200, 'temp_aussen': 12, 'temp_Vl': -8, },
    {'tsp': 1318668480, 'temp_aussen': 13, 'temp_Vl': -7, },
    {'tsp': 1318685760, 'temp_aussen': 14, 'temp_Vl': -6, },
    {'tsp': 1318703040, 'temp_aussen': 15, 'temp_Vl': -5, },
    {'tsp': 1318720320, 'temp_aussen': 16, 'temp_Vl': -4, },
    {'tsp': 1318737600, 'temp_aussen': 17, 'temp_Vl': -3, },
    {'tsp': 1318754880, 'temp_aussen': 18, 'temp_Vl': -2, },
    {'tsp': 1318772160, 'temp_aussen': 19, 'temp_Vl': -1, },
    {'tsp': 1318789440, 'temp_aussen': 20, 'temp_Vl': 0,  },
    {'tsp': 1318806720, 'temp_aussen': 21, 'temp_Vl': 1,  },
    {'tsp': 1318824000, 'temp_aussen': 22, 'temp_Vl': 2,  },
    {'tsp': 1318841280, 'temp_aussen': 23, 'temp_Vl': 3,  },
    {'tsp': 1318858560, 'temp_aussen': 24, 'temp_Vl': 4,  },
    {'tsp': 1318875840, 'temp_aussen': 25, 'temp_Vl': 5,  },
    {'tsp': 1318893120, 'temp_aussen': 26, 'temp_Vl': 6,  },
    {'tsp': 1318910400, 'temp_aussen': 27, 'temp_Vl': 7,  },
    {'tsp': 1318927680, 'temp_aussen': 28, 'temp_Vl': 8,  },
    {'tsp': 1318944960, 'temp_aussen': 29, 'temp_Vl': 9,  },
    {'tsp': 1318962240, 'temp_aussen': 30, 'temp_Vl': 10, },
    {'tsp': 1318979520, 'temp_aussen': 31, 'temp_Vl': 11, },
    {'tsp': 1318996800, 'temp_aussen': 32, 'temp_Vl': 12, },
    {'tsp': 1319014080, 'temp_aussen': 33, 'temp_Vl': 13, },
    {'tsp': 1319031360, 'temp_aussen': 34, 'temp_Vl': 14, },
    {'tsp': 1319048640, 'temp_aussen': 35, 'temp_Vl': 15, },
    {'tsp': 1319065920, 'temp_aussen': 36, 'temp_Vl': 16, },
    {'tsp': 1319083200, 'temp_aussen': 37, 'temp_Vl': 17, },
    {'tsp': 1319100480, 'temp_aussen': 38, 'temp_Vl': 18, },
    {'tsp': 1319117760, 'temp_aussen': 39, 'temp_Vl': 19, },
    {'tsp': 1319135040, 'temp_aussen': 40, 'temp_Vl': 20, },
    {'tsp': 1319152320, 'temp_aussen': 41, 'temp_Vl': 21, },
    {'tsp': 1319169600, 'temp_aussen': 42, 'temp_Vl': 22, },
    {'tsp': 1319186880, 'temp_aussen': 43, 'temp_Vl': 23, },
    {'tsp': 1319204160, 'temp_aussen': 44, 'temp_Vl': 24, },
    {'tsp': 1319221440, 'temp_aussen': 45, 'temp_Vl': 25, },
    {'tsp': 1319238720, 'temp_aussen': 46, 'temp_Vl': 26, },
    {'tsp': 1319256000, 'temp_aussen': 47, 'temp_Vl': 27, },
    {'tsp': 1319273280, 'temp_aussen': 48, 'temp_Vl': 28, },
    {'tsp': 1319290560, 'temp_aussen': 49, 'temp_Vl': 29, },
    {'tsp': 1319307840, 'temp_aussen': 50, 'temp_Vl': 30, },
    {'tsp': 1319325120, 'temp_aussen': 51, 'temp_Vl': 31, },
    {'tsp': 1319342400, 'temp_aussen': 52, 'temp_Vl': 32, },
    {'tsp': 1319359680, 'temp_aussen': 53, 'temp_Vl': 33, },
    {'tsp': 1319376960, 'temp_aussen': 54, 'temp_Vl': 34, },
    {'tsp': 1319394240, 'temp_aussen': 55, 'temp_Vl': 35, },
    {'tsp': 1319411520, 'temp_aussen': 56, 'temp_Vl': 36, },
    {'tsp': 1319428800, 'temp_aussen': 57, 'temp_Vl': 37, },
    {'tsp': 1319446080, 'temp_aussen': 58, 'temp_Vl': 38, },
    {'tsp': 1319463360, 'temp_aussen': 59, 'temp_Vl': 39, 'uhrzeit': datetime.time(18), 'datum': datetime.date(2011, 10, 24) }]

set_data_entries = [ ('test_user', 
                      'Hzg:TempEinsatz', 
                      str(val-5),
                      str(val),
                      datetime.datetime(2011, 10, 24, 13, val), )
                     for val in range(0, 50, 5) ]
                      
def add_get_data_entries_to_db(transaction, session):
    transaction.begin()
    for entry in get_data_entries:
        session.add(PulledData(entry))
    transaction.commit()

def add_set_data_entries_to_db(transaction, session):
    transaction.begin()
    for entry in set_data_entries:
        session.add(DataToSet(*entry))
    transaction.commit()

