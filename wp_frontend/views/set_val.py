# -*- coding: utf-8 -*-
import os.path

import deform
import transaction
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from wp_frontend import settings
from wp_frontend.models import DBSession, get_data, helpers
from wp_frontend.models.set_data import DataToSet, setable
from wp_frontend.views import forms


class SetValObserver(forms.FormEvaluatorObserver):

    def __init__(self, current_data):
        self.current_data = current_data

    def _observe_form_evaluated(self, subj):
        self.extract_vals_from_form(subj)
    
    def extract_vals_from_form(self, subj):
        attr = helpers.map_to_beautifull_names[subj.appstruct['attr']]
        newval = subj.appstruct['newval']
        oldval = self.current_data.__getattribute__(attr)
        user = authenticated_userid(subj.request)
        self._make_and_add_entry(user, attr, newval, oldval)

    def _make_and_add_entry(self, user, attr, newval, oldval):
        transaction.begin()
        entry = DataToSet(user, attr, newval, oldval)
        DBSession.add(entry)
        transaction.commit()

@view_config(route_name='view_set_val', permission='user',
             renderer=os.path.join(settings.templates_dir, 'set_val.pt'))
def view_set_val(request):

    current_data = get_data.CurrentData(setable, DBSession, beauty_names=True)
    current_data.fetch_data()

    svo = SetValObserver(current_data)
    new_form = forms.NewFormRenderer()
    
    fes = forms.FormEvaluatorSubject(request, forms.set_val_form)
    fes.add_observer(new_form)
    fes.add_observer(svo)
    
    fes.evaluate_form()

    return {'current_data': current_data, 
            'form': new_form.form,
            'log': get_log(), 
            'resources': forms.form_resources(forms.set_val_form),
            }


def get_log():
    log = DataToSet.get_latest(DBSession, 10)
    if len(log) == 0:
        return None
    return log
