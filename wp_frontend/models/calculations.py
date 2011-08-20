from wp_frontend.models.get_data import PulledData

def calc_currKW(temp_Vl):
    if temp_Vl < 40:
        return (0.06 * temp_Vl) + 0.5
    elif (temp_Vl > 40) and (temp_Vl < 50):
        return (0.08 * temp_Vl) - 0.3
    return (0.1 * temp_Vl) - 1.3

class CurrKW(object):
    name = 'currKW'
    needed_columns = [PulledData.temp_Vl]
    calc = staticmethod(calc_currKW)

class DeltaVlRl(object):
    name = 'deltaVlRl'
    needed_columns = [PulledData.temp_Vl, PulledData.temp_Rl]
    @staticmethod
    def calc(temp_Vl, temp_Rl):
        return temp_Vl - temp_Rl

class DeltaWQea(object):
    name = 'deltaWQea'
    needed_columns = [PulledData.temp_WQein, PulledData.temp_WQaus]
    @staticmethod
    def calc(temp_WQein, temp_WQaus):
        return temp_WQein - temp_WQaus

available_calculations = [CurrKW, DeltaVlRl, DeltaWQea]

def register_all_calculations():
    from wp_frontend.models.column_calculator import ColumnCalculator
    map(ColumnCalculator.register_calculation, available_calculations)
