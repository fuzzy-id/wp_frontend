# -*- coding: utf-8 -*-
import colander
import deform
from wp_frontend.models import helpers, set_data
from wp_frontend.security import PASSWD


class FormEvaluatorSubject(object):

    states = { 0: 'not_evaluated',
               1: 'no_submission',
               2: 'form_invalid',
               3: 'form_evaluated' }

    def __init__(self, request, form):
        self.request = request
        self.form = form
        self.observers = []
        self.appstruct = None
        self.exception = None
        self._state = 0

    @property
    def state(self):
        return self.states[self._state]

    @state.setter
    def state(self, new_state):
        self._state = new_state
        self._update_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def _update_observers(self):
        for observer in self.observers:
            observer.notify(self)

    def evaluate_form(self):
        if submit_msg in self.request.params:
            try:
                self._extract_values()
                self.state = 3
            except deform.ValidationFailure, e:
                self.exception = e
                self.state = 2
        else:
            self.state = 1

    def _extract_values(self):
        controls = self.request.params.items()
        self.appstruct = self.form.validate(controls)

class FormEvaluatorObserver(object):

    def notify(self, subj):
        if subj.state == 'no_submission':
            self._observe_no_submission(subj)
        elif subj.state == 'form_invalid':
            self._observe_form_invalid(subj)
        elif subj.state == 'form_evaluated':
            self._observe_form_evaluated(subj)
        else:
            raise Exception('unknown state')

    def _observe_form_evaluated(self, subj):
        pass

    def _observe_form_invalid(self, subj):
        pass

    def _observe_no_submission(self, subj):
        pass

class NewFormRenderer(FormEvaluatorObserver):
    
    def __init__(self, default_values={}):
        self.form = None
        self.default_values = default_values

    def _observe_form_evaluated(self, subj):
        self.form = subj.form.render(appstruct=subj.appstruct)

    def _observe_form_invalid(self, subj):
        self.form = subj.exception.render()

    def _observe_no_submission(self, subj):
        self.form = subj.form.render(appstruct=self.default_values)

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

_user_graph_choices = [ (attr, helpers.map_to_beautifull_names[attr], )
                        for attr in helpers.plotable_fields ]

class UserGraphSchema(colander.Schema):
    attr_list = colander.SchemaNode(colander.Sequence(),
                                    widget=deform.widget.CheckboxChoiceWidget(
            values=_user_graph_choices))

_user_graph_schema = UserGraphSchema()
user_graph_form = deform.Form(_user_graph_schema, method="GET",
                              buttons=(submit_msg, ))

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
