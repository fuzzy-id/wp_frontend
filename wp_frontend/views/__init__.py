# -*- coding: utf-8 -*-
import os.path

from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.url import route_url, route_path
from pyramid.view import view_config

from wp_frontend import settings
from wp_frontend.models import DBSession, get_data


@view_config(route_name='view_logout')
def view_logout(request):
    headers = forget(request)
    return HTTPFound(location = route_path('view_wp', 
                                          request),
                     headers = headers)

@view_config(route_name='view_wp')
def view_wp(request):
    return HTTPFound(location = route_path('view_home', request))

@view_config(route_name='view_home', permission='user', 
             renderer=os.path.join(settings.templates_dir, 'home.pt'))
def view_home(request):
    needed_columns = ['version', 'datum_version', 'betriebsmodus',
                      'temp_aussen', 'temp_aussen24', 'temp_aussen1',
                      'temp_RlSoll', 'temp_Rl', 'temp_Vl', 'ww_TempSoll',
                      'ww_TempIst', 'temp_raum', 'temp_raum1', 'temp_WQein',
                      'temp_WQaus', 'temp_Verdampfer', 'temp_Kondensator',
                      'temp_Saugleitung', 'druck_Verdampfer',
                      'druck_Kondensator', 'uhrzeit', 'datum',
                      'betriebsstunden', 'DO_buffer', 'DI_buffer',
                      'currKW', 'deltaVlRl', 'deltaWQea']
    current_data = get_data.CurrentData(needed_columns, DBSession)
    current_data.fetch_data()
    return {'current_data': current_data, }
