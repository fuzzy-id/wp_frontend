# -*- coding: utf-8 -*-
import os.path

import deform
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.url import route_url
from pyramid.view import view_config

from wp_frontend import settings
from wp_frontend.models import DBSession, get_data, helpers
from wp_frontend.views.forms import login_form, submit_msg


@view_config(route_name='view_logout')
def view_logout(request):
    headers = forget(request)
    return HTTPFound(location = route_url('view_wp', 
                                          request),
                     headers = headers)

@view_config(route_name='view_login',
             renderer=os.path.join(settings.templates_dir, 'login.pt'))
def view_login(request):
    if request.url == route_url('view_login', request):
        came_from = request.params.get('came_from', '/')
    else:
        came_from = request.params.get('came_from', request.url)

    if submit_msg in request.params:
        controls = request.params.items()
        try:
            appstruct = login_form.validate(controls)
        except deform.ValidationFailure, e:
            appstruct={'came_from': came_from}
            return {'form': e.render()}

        headers = remember(request, appstruct['user'])
        return HTTPFound(location = came_from, headers = headers)

    return { 'url': request.application_url + '/view_login',
             'form': login_form.render(appstruct={'came_from': came_from}) }

@view_config(route_name='view_wp')
def view_wp(request):
    return HTTPFound(location = route_url('view_home', request))

@view_config(route_name='view_home', permission='user', 
             renderer=os.path.join(settings.templates_dir, 'home.pt'))
def view_home(request):
    needed_columns = ['version', 'datum_version', 'betriebsmodus',
                      'temp_aussen', 'temp_aussen24', 'temp_aussen1',
                      'temp_RlSoll', 'temp_Rl', 'temp_Vl', 'temp_WWSoll',
                      'temp_WW', 'temp_raum', 'temp_raum1', 'temp_WQein',
                      'temp_WQaus', 'temp_Verdampfer', 'temp_Kondensator',
                      'temp_Saugleitung', 'druck_Verdampfer',
                      'druck_Kondensator', 'uhrzeit', 'datum',
                      'betriebsstunden', 'DO_buffer', 'DI_buffer',
                      'currKW', 'deltaVlRl', 'deltaWQea']
    current_data = get_data.CurrentData(needed_columns, DBSession)
    current_data.fetch_data()

    ret_dict = {'current_data': current_data, }
    return ret_dict
