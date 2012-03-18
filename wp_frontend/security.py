# -*- coding: utf-8 -*-

PASSWD = None
GROUPS = None

def make_groupfinder(credential_file):
    credentials = {}
    execfile(credential_file, {}, credentials)
    global PASSWD
    PASSWD = credentials['PASSWD']
    global GROUPS
    GROUPS = credentials['GROUPS']

    def groupfinder(userid, request):
        if userid in PASSWD:
            return GROUPS.get(userid, [])

    return groupfinder
