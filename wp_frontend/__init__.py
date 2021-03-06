# -*- coding: utf-8 -*-
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import wp_frontend.views
from wp_frontend.models import initialize_sql
from wp_frontend.security import make_groupfinder


def main(global_config, sql_init_function=initialize_sql, **settings):
    " This function returns a Pyramid WSGI application. "
    engine = engine_from_config(settings, 'sqlalchemy.')
    sql_init_function(engine)
    authn_policy = AuthTktAuthenticationPolicy(
        'D89neb7:men:rabp_glc84', callback=make_groupfinder(
            settings['credentials']
            ))
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory='wp_frontend.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.add_static_view('static', 'wp_frontend:static')
    # cache for three months:
    config.add_static_view('deform_static', 'deform:static',
                           cache_max_age=(3 * 31 * 24 * 60 * 60))
    
    config.add_route('view_wp', '/')
    config.add_route('view_home', '/home')
    config.add_route('view_graph', '/graph/{graph_name}/*attrs')
    config.add_route('view_choose_graph_attrs', '/user_graph')
    config.add_route('plots', '/plots/{img_name}')
    config.add_route('view_set_val', '/set_val')
    config.add_route('view_status', '/status')
    config.add_route('new_backup_template', '/backup/new_template')
    config.add_route('view_backup', '/backup/{template}')
    config.add_route('edit_backup', '/backup/{template}/edit')
    config.add_route('view_login', '/login')
    config.add_route('view_logout', '/logout')

    config.add_view('wp_frontend.views.login.view_login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer='templates/login.pt')

    config.scan()
    return config.make_wsgi_app()

from pyramid.events import subscriber, BeforeRender
from pyramid.renderers import get_renderer

@subscriber(BeforeRender)
def add_base_template(event):
    event.update({
            'base': get_renderer('templates/base.pt').implementation(), 
            'blocks': get_renderer('templates/blocks.pt').implementation(), 
            })
