# -*- coding: utf-8 -*-
import os.path

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.url import route_url
from pyramid.view import view_config

from wp_frontend import settings
from wp_frontend.views import forms


@view_config(route_name='view_login',
             renderer=os.path.join(settings.templates_dir, 'login.pt'))
def view_login(request):
    if request.url == route_url('view_login', request):
        came_from = request.params.get('came_from', '/')
    else:
        came_from = request.params.get('came_from', request.url)

    resp_gen = LoginResponseGenerator(came_from)
    fes = forms.FormEvaluatorSubject(request, forms.login_form)
    fes.add_observer(resp_gen)
    fes.evaluate_form()
    return resp_gen.response

class LoginResponseGenerator(forms.FormEvaluatorObserver):

    def __init__(self, came_from):
        self.response = None
        self.came_from = came_from

    def _observe_form_evaluated(self, subj):
        headers = remember(subj.request, 
                           subj.appstruct['user'])
        self.response = HTTPFound(location=self.came_from,
                                  headers=headers)

    def _observe_form_invalid(self, subj):
        self.response = {'form': subj.exception.render(), }

    def _observe_no_submission(self, subj):
        self.response = { 'url': subj.request.application_url + '/view_login',
                          'form': forms.login_form.render(appstruct={'came_from': 
                                                                     self.came_from, }),
                          }
