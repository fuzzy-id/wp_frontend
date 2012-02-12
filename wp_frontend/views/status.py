# -*- coding: utf-8 -*-

import os.path
from subprocess import Popen, PIPE

from wp_frontend import settings
from pyramid.view import view_config

@view_config(route_name="view_status", permission='user',
             renderer=os.path.join(settings.templates_dir, 'status.pt'))
def view_status(request):
    uptime = Popen(('uptime', ), stdout=PIPE)
    df = Popen(('df', '-h', ), stdout=PIPE)

    stats = { 'uptime': 'Error while querying uptime!',
              'df': (('Error while querying free disk space!', ), )
        }

    if uptime.wait() == 0:
        stats['uptime'] = ''.join(uptime.stdout)
    if df.wait() == 0:
        stats['df'] = [ l.split(None, 5) for l in  df.stdout ]
    return stats

@view_config(route_name="view_backup", permission='user',
             renderer=os.path.join(settings.templates_dir, 'status.pt'))
def view_backup(request):
    return {}
