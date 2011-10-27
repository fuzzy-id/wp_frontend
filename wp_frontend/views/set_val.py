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


class SetValHandler(object):
    
    def extract_vals_from_form(self, appstruct):
        attr = helpers.map_to_beautifull_names[appstruct['attr']]
        newval = appstruct['newval']
        oldval = appstruct['current_data'].__getattribute__(attr)
        user = appstruct['user']
        transaction.begin()
        entry = DataToSet(user, attr, newval, oldval)
        DBSession.add(entry)
        transaction.commit()

    def as_dict(self):
        return {}

@view_config(route_name='view_set_val', permission='user',
             renderer=os.path.join(settings.templates_dir, 'set_val.pt'))
def view_set_val(request):

    current_data = get_data.CurrentData(setable, DBSession, beauty_names=True)
    ret_dict = {'current_data': current_data, }
    current_data.fetch_data()

    feh = forms.FormEvaluatorAndHandler(forms.set_val_form, SetValHandler())

    feh.handle_request(request, pass_to_handler={'user': authenticated_userid(request),
                                                 'current_data': current_data, })
    ret_dict['form'] = feh.new_rendered_form
    ret_dict['log'] = get_log()

    return ret_dict

def get_log():
    log = DataToSet.get_latest(DBSession, 10)
    if len(log) == 0:
        return None
    return log
