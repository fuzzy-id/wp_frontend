# -*- coding: utf-8 -*-

import os.path
from subprocess import Popen, PIPE

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from wp_frontend import settings
from wp_frontend.views import forms
from wp_frontend.models import DBSession
from wp_frontend.models.backup import BackupTemplate

@view_config(route_name="view_status", permission='user',
             renderer=os.path.join(settings.templates_dir, 'status.pt'))
def view_status(request):
    uptime = Popen(('uptime', ), stdout=PIPE)
    df = Popen(('df', '-h', ), stdout=PIPE)

    stats = { 
        'uptime': 'Error while querying uptime!',
        'df': (('Error while querying free disk space!', ), ),
        'sidebar': get_renderer(
            '../templates/status_sidebar.pt').implementation(),
        'templates': BackupTemplate.get_template_names(DBSession)
        }

    if uptime.wait() == 0:
        stats['uptime'] = ''.join(uptime.stdout)
    if df.wait() == 0:
        stats['df'] = [ l.split(None, 5) for l in  df.stdout 
                        if (('Filesystem' in l)
                            or ('ubi0:rootfs' in l)
                            or ('/dev/mmcblk0p1' in l)
                            or ('/dev/mmcblk0p2' in l)) ]
    return stats

@view_config(route_name="view_backup", permission='user',
             renderer=os.path.join(settings.templates_dir, 'backup.pt'))
def view_backup(request):
    template = request.matchdict['template']
    backup_template = BackupTemplate.get_template_by_name(DBSession, template)
    return { 
        'sidebar': get_renderer(
            os.path.join(settings.templates_dir, 'status_sidebar.pt')
            ).implementation(),
        'templates': BackupTemplate.get_template_names(DBSession),
        'template': backup_template,
        }

@view_config(route_name="new_backup_template", permission='user',
             renderer='wp_frontend:templates/backup_edit.pt')
def new_backup_template(request):
    if forms.submit_msg in request.params:
        controls = request.params.items()
        appstr = forms.backup_form.validate(controls)
        DBSession.add(BackupTemplate(appstr['name'],
                                     appstr['root'],
                                     appstr['excludes']))
        return HTTPFound(location=request.route_path('view_backup', 
                                                     template=appstr['name']))
    deform_resources = forms.backup_form.get_widget_resources()
    resources = {
        'css': [ 'deform:static/' + deform_css
                 for deform_css in deform_resources['css']],
        'js': [ 'deform:static/' + deform_js
                 for deform_js in deform_resources['js']]
        }
    resources['css'].append('deform:static/css/beautify.css')

    return {
        'sidebar': get_renderer(
            'wp_frontend:templates/status_sidebar.pt').implementation(),
        'templates': BackupTemplate.get_template_names(DBSession),
        'form': forms.backup_form.render(),
        'resources': resources,
        }
