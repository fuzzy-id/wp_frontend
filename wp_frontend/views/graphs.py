# -*- coding: utf-8 -*-
import os.path

import deform
from pyramid.view import view_config
from wp_frontend import settings
from wp_frontend.models import DBSession, get_data
from wp_frontend.views import plots, wp_datetime
from wp_frontend.views.forms import timespan_form, submit_msg


needed_columns = {
    'hzg_ww': ('tsp', 'temp_aussen', 'temp_einsatz', 'temp_Vl',
               'temp_RlSoll', 'temp_Rl', 'temp_WW', ),
    'erdsonde': ('tsp', 'temp_WQein', 'temp_WQaus', 'deltaWQea', ),
    'vorl_kondens': ('tsp', 'temp_Kondensator', 'temp_Vl',
                     'deltaKondensVl', ),
    'wqaus_verdamp': ('tsp', 'temp_WQaus', 'temp_Verdampfer',
                      'deltaWQaVerdamp'),
    }


@view_config(route_name='view_graph', permission='user',
             renderer=os.path.join(settings.templates_dir, 'graph.pt'))
def view_graph(request):

    graph_name = request.matchdict['graph_name']
    
    timespan = wp_datetime.TimespanWithResolution()

    ret_dict = {}
    ret_dict['timespan'] = timespan
    ret_dict['vals_available'] = False

    if submit_msg in request.params:
        controls = request.params.items()
        try:
            appstruct = timespan_form.validate(controls)
        except deform.ValidationFailure, e:
            ret_dict['form'] = e.render()
            return ret_dict
        timespan.extract_vals_from_form(appstruct)

    ret_dict['form'] = timespan_form.render(appstruct=timespan.as_dict())

    columns = needed_columns[graph_name]

    number, values = get_data.PulledData.get_values_in_timespan(
        DBSession, columns, timespan)

    timespan.resolution = number

    if len(values) != 0:
        ret_dict['vals_available'] = True
        img = plots.make_plot(columns, values)
        ret_dict['img'] = request.route_path('plots',
                                             img_name=os.path.basename(img))
    return ret_dict
