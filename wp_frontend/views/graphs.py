# -*- coding: utf-8 -*-
import os.path

from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.view import view_config

from wp_frontend import settings
from wp_frontend.models import DBSession, get_data, helpers
from wp_frontend.views import plots, wp_datetime, forms


class PredefinedGraph(forms.FormEvaluatorObserver):
    
    needed_columns = {
        'hzg_ww': ('tsp', 'temp_aussen', 'temp_einsatz', 'temp_Vl',
                   'temp_RlSoll', 'temp_Rl', 'temp_WW', ),
        'erdsonde': ('tsp', 'temp_WQein', 'temp_WQaus', 'deltaWQea', ),
        'vorl_kondens': ('tsp', 'temp_Kondensator', 'temp_Vl',
                         'deltaKondensVl', ),
        'wqaus_verdamp': ('tsp', 'temp_WQaus', 'temp_Verdampfer',
                          'deltaWQaVerdamp'),
        }

    def __init__(self, name, attributes=[]):
        self.name = name
        if name == 'user':
            for attr in attributes:
                if attr not in helpers.plotable_fields:
                    raise HTTPBadRequest("Attribute '%s' is not plotable.")
            self.columns = attributes
        else:
            self.columns = self.needed_columns[self.name]
        self.values = []
        self.img_name = None
        self.plot_url = None

    def catch_values(self, timespan):
        self.values = get_data.PulledData.get_values_in_timespan(
            DBSession, self.columns, timespan)

    def create_plot(self):
        if len(self.values) != 0:
            img = plots.make_plot(self.columns, self.values)
            self.img_name = os.path.basename(img)

    def gen_url_to_plot(self, request):
        if self.img_name is not None:
            self.plot_url = request.route_path('plots',
                                               img_name=self.img_name)

class GraphTimespanWithResolutionMediator(object):
    
    def __init__(self, graph, tsp_w_res):
        self.graph = graph
        self.tsp_w_res = tsp_w_res

    def notify(self, subj):
        self.tsp_w_res.notify(subj)
        self.graph.notify(subj)
        self.gen_graph(subj.request)
        
    def gen_graph(self, request):
        self.graph.catch_values(self.tsp_w_res)
        self.graph.create_plot()
        self.graph.gen_url_to_plot(request)

@view_config(route_name='view_graph', permission='user',
             renderer=os.path.join(settings.templates_dir, 'graph.pt'))
def view_graph(request):

    tsp_w_res = wp_datetime.TimespanWithResolution()
    graph = PredefinedGraph(request.matchdict['graph_name'], 
                            request.matchdict['attrs'])
    mediator = GraphTimespanWithResolutionMediator(graph, tsp_w_res)

    new_form = forms.NewFormRenderer(default_values=tsp_w_res.as_dict())
    
    fes = forms.FormEvaluatorSubject(request, forms.get_tsp_w_res_form())
    fes.add_observer(mediator)
    fes.add_observer(new_form)

    fes.evaluate_form()

    return { 'graph': graph,
             'timespan': tsp_w_res,
             'form': new_form.form, }

class UserGraphForwarder(forms.FormEvaluatorObserver):
    
    def __init__(self):
        self.redirect = None
    
    def _observe_form_evaluated(self, subj):
        self.redirect = subj.request.route_path('view_graph', graph_name='user', 
                                       attrs=subj.appstruct['attr_list'])

@view_config(route_name='view_choose_graph_attrs', permission='user',
             renderer=os.path.join(settings.templates_dir, 'user_graph.pt'))
def user_graph(request):
    new_form = forms.NewFormRenderer()
    ug_forw = UserGraphForwarder()

    fes = forms.FormEvaluatorSubject(request, forms.get_user_graph_form())
    fes.add_observer(new_form)
    fes.add_observer(ug_forw)

    fes.evaluate_form()

    if ug_forw.redirect is not None:
        return HTTPFound(location=ug_forw.redirect)
    return { 'form': new_form.form, }
