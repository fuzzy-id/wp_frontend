# -*- coding: utf-8 -*-
from wp_frontend.passwd import PASSWD, GROUPS

def groupfinder(userid, request):
    if userid in PASSWD:
        return GROUPS.get(userid, [])
