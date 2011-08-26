import datetime
import os.path

import deform

from wp_frontend.models import DBSession, get_data
from wp_frontend.views import plots
from wp_frontend.views.forms import timespan_form, submit_msg

def strip_min_ms(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

def view_graph(request):

    graph_name = request.matchdict['graph_name']
    
    ret_dict = {}

    ret_dict['end'] = strip_min_ms(datetime.datetime.now())
    ret_dict['start'] = ret_dict['end'] - datetime.timedelta(days=30)
    ret_dict['vals_available'] = False
    ret_dict['resolution'] = 500

    if submit_msg in request.params:
        controls = request.params.items()
        try:
            appstruct = timespan_form.validate(controls)
        except deform.ValidationFailure, e:
            ret_dict['form'] = e.render()
            return ret_dict
        ret_dict['end'] = appstruct['end']
        ret_dict['start'] = appstruct['start']
        ret_dict['resolution'] = appstruct['resolution']

    ret_dict['form'] = timespan_form.render(
        appstruct={'start': ret_dict['start'],
                   'end': ret_dict['end'],
                   'resolution': ret_dict['resolution'], })

    columns = needed_columns[graph_name]

    number, values = get_data.PulledData.get_values_in_timespan(
        DBSession, columns, ret_dict['start'], ret_dict['end'],
        ret_dict['resolution'])

    ret_dict['resolution'] = number

    if len(values) != 0:
        ret_dict['vals_available'] = True
        img = plots.make_plot(columns, values)
        ret_dict['img'] = request.route_path('plots',
                                             img_name=os.path.basename(img))
    return ret_dict

needed_columns = {
    'hzg_ww': ('tsp', 'temp_aussen', 'temp_einsatz', 'temp_Vl',
               'temp_RlSoll', 'temp_Rl', 'temp_WW', ),
    'erdsonde': ('tsp', 'temp_WQein', 'temp_WQaus', 'deltaWQea', ),
    'vorl_kondens': ('tsp', 'temp_Kondensator', 'temp_Vl',
                     'deltaKondensVl', ),
    'wqaus_verdamp': ('tsp', 'temp_WQaus', 'temp_Verdampfer',
                      'deltaWQaVerdamp'),
    }
