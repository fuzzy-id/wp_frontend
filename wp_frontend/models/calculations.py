# -*- coding: utf-8 -*-
from wp_frontend.models.get_data import PulledData

class BetrHWwPlusHzg(object):
    name = 'betrHWwPlusHzg'
    needed_columns = [PulledData.betr_h_hzg_pu, PulledData.betr_h_ww_pu]
    @staticmethod
    def calc(betr_h_hzg, betr_h_ww):
        return betr_h_hzg + betr_h_ww

class CurrKW(object):
    name = 'currKW'
    needed_columns = [PulledData.temp_Vl]
    @staticmethod
    def calc(temp_Vl):
        if temp_Vl <= 40:
            return (0.06 * temp_Vl) + 0.5
        elif 40 < temp_Vl < 50:
            return (0.08 * temp_Vl) - 0.3
        return (0.1 * temp_Vl) - 1.3

class DeltaVlRl(object):
    name = 'deltaVlRl'
    needed_columns = [PulledData.temp_Vl, PulledData.temp_Rl]
    @staticmethod
    def calc(temp_Vl, temp_Rl):
        return temp_Vl - temp_Rl

class DeltaKondensVl(object):
    name = 'deltaKondensVl'
    needed_columns = [PulledData.temp_Kondensator, PulledData.temp_Vl]
    @staticmethod
    def calc(temp_Kondensator, temp_Vl):
        return temp_Kondensator - temp_Vl

class DeltaWQea(object):
    name = 'deltaWQea'
    needed_columns = [PulledData.temp_WQein, PulledData.temp_WQaus]
    @staticmethod
    def calc(temp_WQein, temp_WQaus):
        return temp_WQein - temp_WQaus

class DeltaWQaVerdamp(object):
    name = 'deltaWQaVerdamp'
    needed_columns = [PulledData.temp_WQaus, PulledData.temp_Verdampfer]
    @staticmethod
    def calc(temp_WQaus, temp_Verdamp):
        return temp_WQaus - temp_Verdamp

available_calculations = [CurrKW, DeltaVlRl, DeltaWQea, DeltaKondensVl,
                          DeltaWQaVerdamp, BetrHWwPlusHzg, ]

def register_all_calculations():
    from wp_frontend.models.column_calculator import ColumnCalculator
    map(ColumnCalculator.register_calculation, available_calculations)
