# -*- coding: utf-8 -*-
import os.path

import deform
from pyramid.view import view_config
from wp_frontend import settings
from wp_frontend.models import DBSession, get_data
from wp_frontend.views import plots, wp_datetime, forms
from wp_frontend.views.forms import timespan_form, submit_msg

class Graph(object):
    
    needed_columns = {
        'hzg_ww': ('tsp', 'temp_aussen', 'temp_einsatz', 'temp_Vl',
                   'temp_RlSoll', 'temp_Rl', 'temp_WW', ),
        'erdsonde': ('tsp', 'temp_WQein', 'temp_WQaus', 'deltaWQea', ),
        'vorl_kondens': ('tsp', 'temp_Kondensator', 'temp_Vl',
                         'deltaKondensVl', ),
        'wqaus_verdamp': ('tsp', 'temp_WQaus', 'temp_Verdampfer',
                          'deltaWQaVerdamp'),
        }

    def __init__(self, name):
        self.name = name
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


@view_config(route_name='view_graph', permission='user',
             renderer=os.path.join(settings.templates_dir, 'graph.pt'))
def view_graph(request):

    timespan = wp_datetime.TimespanWithResolution()
    ret_dict = {'timespan': timespan,
                'vals_available': False, }

    graph = Graph(request.matchdict['graph_name'])
    ret_dict['graph'] = graph

    def gen_graph():
        graph.catch_values(timespan)
        graph.create_plot()
        graph.gen_url_to_plot(request)

    feh = forms.FormEvaluatorAndHandler(timespan_form, timespan)
    feh.handle_request(request, callback=gen_graph)

    ret_dict['form'] = feh.new_rendered_form

    return ret_dict
