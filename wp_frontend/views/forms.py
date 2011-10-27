# -*- coding: utf-8 -*-
import colander
import deform
from wp_frontend.models import helpers, set_data
from wp_frontend.security import PASSWD


class FormEvaluatorAndHandler(object):

    def __init__(self, form, handling_obj):
        self.form = form
        self.handling_obj = handling_obj
        self.new_rendered_form = None

    def handle_request(self, request, pass_to_handler=None, callback=None):
        if submit_msg in request.params:
            self._handle_form(request, pass_to_handler)
        else:
            self.new_rendered_form = self.form.render(appstruct=self.handling_obj.as_dict())
        if callback is not None:
            callback()

    def _handle_form(self, request, pass_to_handler):
        controls = request.params.items()
        try:
            appstruct = self.form.validate(controls)
        except deform.ValidationFailure, e:
            self.new_rendered_form = e.render()
        else:
            if pass_to_handler is not None:
                appstruct.update(pass_to_handler)
            self.handling_obj.extract_vals_from_form(appstruct)
            self.new_rendered_form = self.form.render(appstruct=self.handling_obj.as_dict())        

submit_msg = 'submit'

class LoginSchema(colander.Schema):
    user = colander.SchemaNode(
        colander.String())
    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.PasswordWidget())
    came_from = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget())

def credential_validator(form, value):
    user = value['user']
    if (user not in PASSWD.keys()
        or value['password'] != PASSWD.get(value['user'])):
        exc = colander.Invalid(form, "Username or password invalid!")
        exc['password'] = "Username or password invalid!"
        raise exc

_login_schema = LoginSchema(validator=credential_validator)
login_form = deform.Form(_login_schema, buttons=(submit_msg,))
    

class TimespanSchema(colander.Schema):
    start = colander.SchemaNode(colander.DateTime())
    end = colander.SchemaNode(colander.DateTime())
    resolution = colander.SchemaNode(colander.Integer(),
                                     validator=colander.Range(1, 10000))

def timespan_validator(form, value):
    if value['start'] >= value['end']:
        exc = colander.Invalid(form, 'Start has to be before End')
        exc['end'] = 'Start has to be before End'
        raise exc

_timespan_schema = TimespanSchema(validator=timespan_validator)
timespan_form = deform.Form(_timespan_schema, method="POST",
                            buttons=(submit_msg,))

_set_val_choices = [ (attr, helpers.map_to_beautifull_names[attr], )
                     for attr in set_data.setable ]

class SetValSchema(colander.Schema):
    attr = colander.SchemaNode(colander.String(),
                               widget=deform.widget.SelectWidget(
                                   values=_set_val_choices))
    newval = colander.SchemaNode(colander.String())

def set_val_validator(form, value):
    attr = value['attr']
    if (validate_attr('attr', value['newval']) == False):
        exc = colander.Invalid(form, 'New value not accepted')
        exc['newval'] = 'New value not accepted'
        raise exc

def validate_attr(attr, value):
    return True
    
_set_val_schema = SetValSchema(validator=set_val_validator)
set_val_form = deform.Form(_set_val_schema, method="POST",
                           buttons=(submit_msg, ))
