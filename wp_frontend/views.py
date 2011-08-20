import datetime
import os.path
import tempfile

import colander
import deform
import matplotlib.pyplot as plt
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.url import route_url
from wp_frontend.models import DBSession, get_data
from pyramid.view import view_config

def view_wp(request):
    return HTTPFound(location = route_url('view_home', 
                                          request))

def view_home(request):
    needed_columns = ['version', 'datum_version', 'betriebsmodus',
                      'temp_aussen', 'temp_aussen24', 'temp_aussen1',
                      'temp_RlSoll', 'temp_Rl', 'temp_Vl', 'temp_WWSoll',
                      'temp_WW', 'temp_raum', 'temp_raum1', 'temp_WQein',
                      'temp_WQaus', 'temp_Verdampfer', 'temp_Kondensator',
                      'temp_Saugleitung', 'druck_Verdampfer',
                      'druck_Kondensator', 'uhrzeit', 'datum',
                      'betriebsstunden', 'DO_buffer', 'DI_buffer',
                      'currKW', 'deltaVlRl', 'deltaWQea']
    logged_in = authenticated_userid(request)
    data = get_data.PulledData.get_latest(DBSession, needed_columns)
    if data is not None:
        data = dict(zip(needed_columns, data))
    ret_dict = {'data': data, }
    return ret_dict

def strip_min_ms(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

def timespan_validator(form, value):
    if value['start'] >= value['end']:
        exc = colander.Invalid(form, 'Start has to be before End')
        exc['end'] = 'Start has to be before End'
        raise exc

class TimespanSchema(colander.Schema):
    start = colander.SchemaNode(colander.DateTime())
    end = colander.SchemaNode(colander.DateTime())


def view_hzg_ww(request):
    ret_dict = {}

    ret_dict['end'] = strip_min_ms(datetime.datetime.now())
    ret_dict['start'] = ret_dict['end'] - datetime.timedelta(days=30)
    ret_dict['vals_available'] = False

    schema = TimespanSchema(validator=timespan_validator)
    form = deform.Form(schema, method="GET", buttons=('submit', ))

    if 'submit' in request.params:
        controls = request.params.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            ret_dict['form'] = e.render()
            return ret_dict
        ret_dict['end'] = appstruct['end']
        ret_dict['start'] = appstruct['start']

    ret_dict['form'] = form.render(appstruct={'start': ret_dict['start'],
                                              'end': ret_dict['end']})

    columns = ['tsp', 'temp_aussen', 'temp_einsatz', 'temp_Vl',
               'temp_RlSoll', 'temp_Rl', 'temp_WW']

    values = get_data.PulledData.get_values_in_timespan(DBSession,
                                                        columns,
                                                        ret_dict['start'],
                                                        ret_dict['end'])
    if len(values) != 0:
        ret_dict['vals_available'] = True
        img = make_plot(columns, values)
        ret_dict['img'] = request.route_path('plots',
                                             img_name=os.path.basename(img))
    return ret_dict

def make_plot(columns, values):
    x_axis = [ datetime.datetime.fromtimestamp(d[0]) for d in values ]
    for i in range(1, len(columns)):
        plt.plot(x_axis, [ d[i] for d in values ])

    img = tempfile.mkstemp(prefix='plot-', suffix='.svgz',
                           dir='wp_frontend/plots')
    img = img[1]
    plt.savefig(img)
    return img

def view_set_val(request):
    logged_in = authenticated_userid(request)
    ret_dict = {}
    ret_dict['logged_in'] = logged_in
    return ret_dict

def get_plot(request):
    img_name = request.matchdict['img_name']
    f = open(os.path.join('wp_frontend/plots', img_name))
    response = Response(content_type='image/svg+xml',
                        content_encoding='gzip',
                        app_iter=f)
    return response
             
