import transaction
import datetime
import os.path
import tempfile

import deform
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import authenticated_userid, remember, forget
from pyramid.url import route_url

from wp_frontend.models import DBSession, get_data, map_to_beautifull_names
from wp_frontend.models.set_data import DataToSet, setable
from wp_frontend.views.forms import timespan_form, login_form, submit_msg, set_val_form


def view_logout(request):
    headers = forget(request)
    return HTTPFound(location = route_url('view_wp', 
                                          request),
                     headers = headers)

def view_login(request):
    if request.url == route_url('view_login', request):
        came_from = request.params.get('came_from', '/')
    else:
        came_from = request.params.get('came_from', request.url)

    if submit_msg in request.params:
        controls = request.params.items()
        try:
            appstruct = login_form.validate(controls)
        except deform.ValidationFailure, e:
            appstruct={'came_from': came_from}
            return {'form': e.render()}

        headers = remember(request, appstruct['user'])
        return HTTPFound(location = came_from, headers = headers)

    return { 'url': request.application_url + '/view_login',
             'form': login_form.render(appstruct={'came_from': came_from}) }

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
    data = get_data.PulledData.get_latest(DBSession, needed_columns)
    if data is not None:
        data = dict(zip(needed_columns, data))
    ret_dict = {'data': data, }
    return ret_dict

def strip_min_ms(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

def view_hzg_ww(request):
    ret_dict = {}

    ret_dict['end'] = strip_min_ms(datetime.datetime.now())
    ret_dict['start'] = ret_dict['end'] - datetime.timedelta(days=30)
    ret_dict['vals_available'] = False

    if submit_msg in request.params:
        controls = request.params.items()
        try:
            appstruct = timespan_form.validate(controls)
        except deform.ValidationFailure, e:
            ret_dict['form'] = e.render()
            return ret_dict
        ret_dict['end'] = appstruct['end']
        ret_dict['start'] = appstruct['start']

    ret_dict['form'] = timespan_form.render(appstruct={'start': ret_dict['start'],
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


from matplotlib.font_manager import FontProperties
import matplotlib
matplotlib.use('cairo.svg')
import matplotlib.backends.backend_tkagg as plt

def make_plot(columns, values):

    fig = plt.Figure()
    canvas = plt.FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    
    x_axis = [ datetime.datetime.fromtimestamp(d[0]) for d in values ]
    for i in range(1, len(columns)):
        label = map_to_beautifull_names[columns[i]]
        ax.plot(x_axis, [ d[i] for d in values ], label=label)

    img = tempfile.mkstemp(prefix='plot-', suffix='.svgz',
                           dir='wp_frontend/plots')
    img = img[1]

    fontP = FontProperties()
    fontP.set_size('small')
    fig.autofmt_xdate()

    ax.legend(loc="best", prop=fontP)
    canvas.print_figure(img)
    return img

def get_plot(request):
    img_name = request.matchdict['img_name']
    f = open(os.path.join('wp_frontend/plots', img_name))
    response = Response(content_type='image/svg+xml',
                        content_encoding='gzip',
                        app_iter=f)
    return response

def view_set_val(request):

    current_values = get_data.PulledData.get_latest(DBSession, setable)
    if current_values is not None:
        beauty_setable = [ map_to_beautifull_names[s] for s in setable ]
        current_values = dict(zip(beauty_setable, current_values))

    ret_dict = {'current_values': current_values, }

    if submit_msg in request.params:
        controls = request.params.items()
        try:
            appstruct = set_val_form.validate(controls)
        except deform.ValidationFailure, e:
            ret_dict['form'] = e.render()
            ret_dict['log'] = get_log()
            return ret_dict
        attr = map_to_beautifull_names[appstruct['attr']]
        newval = appstruct['newval']
        if current_values is None:
            oldval = None
        else:
            oldval = current_values[attr]
        user = authenticated_userid(request)
        transaction.begin()
        entry = DataToSet(user, attr, newval, oldval)
        DBSession.add(entry)
        transaction.commit()
        
    ret_dict['form'] = set_val_form.render()
    ret_dict['log'] = get_log()

    return ret_dict

def get_log():
    log = DataToSet.get_latest(DBSession, 10)
    if len(log) == 0:
        return None
    return log
