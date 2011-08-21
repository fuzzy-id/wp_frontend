import colander
import deform
from wp_frontend.security import PASSWD

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

def timespan_validator(form, value):
    if value['start'] >= value['end']:
        exc = colander.Invalid(form, 'Start has to be before End')
        exc['end'] = 'Start has to be before End'
        raise exc

_timespan_schema = TimespanSchema(validator=timespan_validator)
timespan_form = deform.Form(_timespan_schema,
                            method="GET",
                            buttons=(submit_msg, ))

