PASSWD = {'test_user':'password'}
GROUPS = {'test_user':['group:users']}

def groupfinder(userid, request):
    if userid in PASSWD:
        return GROUPS.get(userid, [])
