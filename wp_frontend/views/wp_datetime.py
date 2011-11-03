# -*- coding: utf-8 -*-
import datetime
import time
from wp_frontend.views import forms

def strip_ms(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def convert_to_timestamp(dt):
    return time.mktime(dt.timetuple())

class TimespanWithResolution(forms.FormEvaluatorObserver):
    
    def __init__(self, start=None, end=None, resolution=500):

        if end is None:
            self.end = datetime.datetime.now()
        else:
            self.end = end

        if start is None:
            self.start = self.end - datetime.timedelta(days=30)
        else:
            self.start = start

        self.resolution = resolution

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, dt):
        self._start = strip_ms(dt)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, dt):
        self._end = strip_ms(dt)

    def _observe_form_evaluated(self, subj):
        self._extract_values_from_appstruct(subj.appstruct)

    def _extract_values_from_appstruct(self, appstr):
        self.end = appstr['end']
        self.start = appstr['start']
        self.resolution = appstr['resolution']

    def as_dict(self):
        return {'start': self.start,
                'end': self.end,
                'resolution': self.resolution, }

    def start_as_timestamp(self):
        return convert_to_timestamp(self.start)

    def end_as_timestamp(self):
        return convert_to_timestamp(self.end)

    def __iter__(self):
        start_tsp = int(self.start_as_timestamp())
        end_tsp = int(self.end_as_timestamp())
        step = (end_tsp - start_tsp) / self.resolution

        for avg_start in range(start_tsp, end_tsp, step):
            yield (avg_start, avg_start + step)
