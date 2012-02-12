# -*- coding: utf-8 -*-

from pyramid.view import view_config

@view_config(route_name="view_status", permission='user')
def view_status(request):
    pass
