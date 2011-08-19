from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from wp_frontend.models import initialize_sql

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from wp_frontend.security import groupfinder

def main(global_config, sql_init_function=initialize_sql, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    sql_init_function(engine)
    authn_policy = AuthTktAuthenticationPolicy(
        'foobar', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory='wp_frontend.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)

    config.add_subscriber('wp_frontend.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')

    config.add_static_view('static', 'wp_frontend:static')
    config.add_static_view('deform_static', 'deform:static')
    
    config.add_route('view_wp', '/')
    config.add_view('wp_frontend.views.view_wp', 
                    route_name='view_wp')

    config.add_route('view_home', '/home')
    config.add_view('wp_frontend.views.view_home',
                    route_name='view_home',
                    renderer='templates/home.pt',
                    permission='user')

    config.add_route('view_hzg_ww', '/hzg_ww')
    config.add_view('wp_frontend.views.view_hzg_ww',
                    route_name='view_hzg_ww',
                    renderer='templates/hzg_ww.pt',
                    permission='user')

    config.add_route('plots', '/plots/{img_name}')
    config.add_view('wp_frontend.views.get_plot',
                    route_name='plots',
                    permission='user')
    
    config.add_route('view_set_val', '/set_val')
    config.add_view('wp_frontend.views.view_set_val',
                    route_name='view_set_val',
                    renderer='templates/set_val.pt',
                    permission='user')

    config.add_route('login', '/login')
    config.add_view('wp_frontend.login.login',
                    route_name='login',
                    renderer='templates/login.pt')
    config.add_view('wp_frontend.login.login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer='templates/login.pt')

    config.add_route('logout', '/logout')
    config.add_view('wp_frontend.login.logout',
                    route_name='logout')

    return config.make_wsgi_app()
