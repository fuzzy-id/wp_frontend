# -*- coding: utf-8 -*-

import datetime
import os.path
import tempfile

import matplotlib
matplotlib.use('cairo.svg')

import matplotlib.backends.backend_tkagg as plt
from matplotlib.font_manager import FontProperties
from pyramid.response import Response

from wp_frontend import settings
from wp_frontend.models import helpers
from pyramid.view import view_config

@view_config(route_name='plots', permission='user')
def get_plot(request):
    img_name = request.matchdict['img_name']
    f = open(os.path.join(settings.plots_dir, img_name))
    response = Response(content_type='image/svg+xml',
                        content_encoding='gzip',
                        app_iter=f)
    return response

def make_plot(columns, values):

    fig = plt.Figure()
    canvas = plt.FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    
    x_axis = tuple(datetime.datetime.fromtimestamp(d[0]) for d in values)
    for i in range(1, len(columns)):
        label = helpers.map_to_beautifull_names[columns[i]]
        ax.plot(x_axis, tuple( d[i] for d in values ), label=label)

    img = tempfile.mkstemp(prefix='plot-', suffix='.svgz',
                           dir=settings.plots_dir)
    img = img[1]

    fontP = FontProperties()
    fontP.set_size('small')
    fig.autofmt_xdate()

    ax.legend(loc="best", prop=fontP)
    canvas.print_figure(img)
    return img
