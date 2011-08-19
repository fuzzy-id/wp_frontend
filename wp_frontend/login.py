# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget
from pyramid.url import route_url

from wp_frontend.security import PASSWD

import colander
import deform

def credential_validator(form, value):
    user = value['user']
    if (user not in PASSWD.keys()
        or value['password'] != PASSWD.get(value['user'])):
        exc = colander.Invalid(form, "Username or password invalid!")
        exc['password'] = "Username or password invalid!"
        raise exc

class LoginSchema(colander.Schema):
    user = colander.SchemaNode(
        colander.String())
    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.PasswordWidget())
    came_from = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget())

def login(request):
    if request.url == route_url('login', request):
        came_from = request.params.get('came_from', '/')
    else:
        came_from = request.params.get('came_from', request.url)

    schema = LoginSchema(validator=credential_validator)
    form = deform.Form(schema, buttons=('Login',))
    
    if 'Login' in request.params:
        controls = request.params.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            appstruct={'came_from': came_from}
            return {'form': e.render()}

        headers = remember(request, appstruct['user'])
        return HTTPFound(location = came_from, headers = headers)

    return { 'url': request.application_url + '/login',
             'form': form.render(appstruct={'came_from': came_from}) }

def logout(request):
    headers = forget(request)
    return HTTPFound(location = route_url('view_wp', 
                                          request),
                     headers = headers)
