import re

def _flatten_list(the_list):
    result = []
    for item in the_list:
        if type(item) is list:
            result.extend(_flatten_list(item))
        else:
            result.append(item)
    return result

class ColumnCalculator(object):

    available_calculations = {}

    @classmethod
    def register_calculation(cls, calculation):
        cls.available_calculations[calculation.name] = calculation

    def __init__(self, columns):
        self.columns = columns
        self.needed_calculation = []
        self._find_needed_calculations()

    def _find_needed_calculations(self):
        regex = "(%s)" % ('|'.join(self.available_calculations.keys()))
        if len(regex) == 2:
            return

        calculation_re = re.compile(regex)

        for i in range(len(self.columns)):
            if calculation_re.match(self.columns[i]) is not None:
                c_name = calculation_re.match(self.columns[i]).group()
                calculation = self.available_calculations[c_name]
                self.needed_calculation.append((i, calculation, ))

    def add_entries(self, entries):
        for index, calculation in self.needed_calculation:
            entries[index] = calculation.needed_columns
        return _flatten_list(entries)

    def calculate_entries(self, entries):
        if entries is None:
            return None
        entries = list(entries)
        for index, calculation in self.needed_calculation:
            args_num = len(calculation.needed_columns)
            args_end = index + args_num
            args = entries[index:args_end]
            val = calculation.calc(*args)
            entries = entries[:index] + [val] + entries[args_end:]
        return tuple(entries)
