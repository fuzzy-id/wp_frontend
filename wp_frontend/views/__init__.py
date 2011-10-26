# -*- coding: utf-8 -*-
import os.path

import deform
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid, remember, forget
from pyramid.url import route_url
from pyramid.view import view_config
from wp_frontend import settings
from wp_frontend.models import DBSession, get_data, map_to_beautifull_names
from wp_frontend.models.set_data import DataToSet, setable
from wp_frontend.views.forms import login_form, submit_msg, set_val_form


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
    data = get_data.PulledData.get_latest(DBSession, needed_columns)
    if data is not None:
        data = dict(zip(needed_columns, data))
    ret_dict = {'data': data, }
    return ret_dict

@view_config(route_name='view_set_val', permission='user',
             renderer=os.path.join(settings.templates_dir, 'set_val.pt'))
def view_set_val(request):

    current_values = get_data.PulledData.get_latest(DBSession, setable)
    if current_values is not None:
        beauty_setable = [ map_to_beautifull_names[s] for s in setable ]
        current_values = dict(zip(beauty_setable, current_values))

    ret_dict = {'current_values': current_values, }

    if submit_msg in request.params:
        controls = request.params.items()
        try:
            appstruct = set_val_form.validate(controls)
        except deform.ValidationFailure, e:
            ret_dict['form'] = e.render()
            ret_dict['log'] = get_log()
            return ret_dict
        attr = map_to_beautifull_names[appstruct['attr']]
        newval = appstruct['newval']
        if current_values is None:
            oldval = None
        else:
            oldval = current_values[attr]
        user = authenticated_userid(request)
        transaction.begin()
        entry = DataToSet(user, attr, newval, oldval)
        DBSession.add(entry)
        transaction.commit()
        
    ret_dict['form'] = set_val_form.render()
    ret_dict['log'] = get_log()

    return ret_dict

def get_log():
    log = DataToSet.get_latest(DBSession, 10)
    if len(log) == 0:
        return None
    return log
