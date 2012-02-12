# -*- coding: utf-8 -*-

import os.path

from wp_frontend import settings
from pyramid.view import view_config

@view_config(route_name="view_status", permission='user',
             renderer=os.path.join(settings.templates_dir, 'status.pt'))
def view_status(request):
    return {}

@view_config(route_name="view_backup", permission='user',
             renderer=os.path.join(settings.templates_dir, 'status.pt'))
def view_backup(request):
    return {}
