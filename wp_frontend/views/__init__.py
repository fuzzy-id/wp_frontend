# -*- coding: utf-8 -*-
import os.path

from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.url import route_url, route_path
from pyramid.view import view_config

from wp_frontend import settings
from wp_frontend.models import DBSession, get_data
from wp_frontend.views.wp_datetime import TimespanWithResolution
import datetime


@view_config(route_name='view_logout')
def view_logout(request):
    headers = forget(request)
    return HTTPFound(location = route_path('view_wp', 
                                          request),
                     headers = headers)

@view_config(route_name='view_wp')
def view_wp(request):
    return HTTPFound(location = route_path('view_home', request))

@view_config(route_name='view_home', permission='user', 
             renderer=os.path.join(settings.templates_dir, 'home.pt'))
def view_home(request):
    needed_columns = ['version', 'datum_version', 'betriebsmodus',
                      'temp_aussen', 'temp_aussen24', 'temp_aussen1',
                      'temp_RlSoll', 'temp_Rl', 'temp_Vl', 'ww_TempSoll',
                      'ww_TempIst', 'temp_raum', 'temp_raum1', 'temp_WQein',
                      'temp_WQaus', 'temp_Verdampfer', 'temp_Kondensator',
                      'temp_Saugleitung', 'druck_Verdampfer',
                      'druck_Kondensator', 'uhrzeit', 'datum',
                      'DO_buffer', 'DI_buffer', 'currKW', 'deltaVlRl', 
                      'deltaWQea', 'betrHWwPlusHzg', ]
    current_data = get_data.CurrentData(needed_columns, DBSession)
    current_data.fetch_data()
    
    if current_data.betrHWwPlusHzg is not None:
        now = datetime.datetime.now()
        one_year_ago = datetime.datetime(now.year - 1, now.month, now.day, 
                                         now.hour, now.minute)
        tsp_w_res_one_year_ago = TimespanWithResolution(
            start=one_year_ago - datetime.timedelta(minutes=30),
            end=one_year_ago + datetime.timedelta(minutes=30),
            resolution=1)
        betr_h_ww_plus_hzg_one_year_ago = get_data.PulledData.get_values_in_timespan(
            DBSession, ['betrHWwPlusHzg', ], tsp_w_res_one_year_ago)
        if len(betr_h_ww_plus_hzg_one_year_ago) == 1:
            current_data.betrHWwPlusHzg -= betr_h_ww_plus_hzg_one_year_ago[0][0]
            setattr(current_data, 'verbrauch', 
                    current_data.betrHWwPlusHzg * 1.9177)
        else:
            setattr(current_data, 'verbrauch', None)
    else:
        setattr(current_data, 'verbrauch', None)
            
        
    
    return {'current_data': current_data, }
