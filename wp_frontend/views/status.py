# -*- coding: utf-8 -*-

from pyramid.view import view_config

@view_config(route_name="view_status", permission='user',
             renderer=os.path.join(settings.templates_dir, 'status.pt'))
def view_status(request):
    pass
