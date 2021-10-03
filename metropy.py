import re
import json
import csv

class MetroCalc(object):
    standMean = 2
    def rounding(self, integer:int=None, middle_mean=standMean) -> int:
        if not integer is None:
            integer = str(integer)
            int_match = re.findall(r"\d*\.[0]*[0-9]{1," + str(middle_mean + 1) + "}", integer)

            if (int(int_match[0][-1]) >= 5) and (len(int_match[0]) - int_match[0].count('0') >= 4):
                integer = int_match[0][:-2] + str(int(int_match[0][-2]) + 1)
                integer = float(integer)
            else:
                integer = float(int_match[0])
                
            return integer
        else:
            pass #exception

class MetroFReader():
    pass

class MetroPy(object):
    __calc = MetroCalc()

    def __init__(self, indications:dict=None, hash_sys_error:dict=None):
        self.ethalons    = indications.keys()
        self.indications = indications
        self.mpy_table   = dict([])

        for ethalon in self.indications.keys():
            sys_error = None

            if (not hash_sys_error is None) and (hash_sys_error.keys() == self.indications.keys()):
                sys_error = hash_sys_error[ethalon]
            else:
                sys_error = None

            self.mpy_table[ethalon] = {
                'index'      : [index for index in range(1, len(self.indications[ethalon]) + 1)],
                'indication' : [indication for indication in self.indications[ethalon]],
                'abs_error'  : [],
                'abs_middle' : None,
                'sys_error'  : sys_error,
                'rand_error' : [],
                'dispersion' : None,
            }

    def abs_error(self, ethalon:list=None):
        if ethalon is None:
            self.error('abs_error')
        else:
            for indication in self.mpy_table[ethalon]['indication']:
                dynamic_abs = MetroPy.__calc.rounding(indication - ethalon)
                self.mpy_table[ethalon]['abs_error'].append(dynamic_abs)
    
    def abs_middle(self, ethalon:list=None):
        if ethalon is None:
            self.error('abs_middle')
        else:
            abs_sum = sum(self.mpy_table[ethalon]['abs_error'])
            ind_count = self.mpy_table[ethalon]['index'][-1]
            self.mpy_table[ethalon]['abs_middle'] = MetroPy.__calc.rounding(abs_sum / ind_count)

    def sys_error(self, ethalon:list=None):
        if ethalon is None:
            self.error('sys_error')
        else:
            self.mpy_table[ethalon]['sys_error'] = self.mpy_table[ethalon]['abs_middle']

    def dispersion(self, ethalon:list=None):
        if ethalon is None:
            self.error('dispersion')
        else:
            rand_sum = sum([rand**2 for rand in self.mpy_table[ethalon]['rand_error']])
            ind_count = self.mpy_table[ethalon]['index'][-1]
            self.mpy_table[ethalon]['dispersion'] = MetroPy.__calc.rounding(rand_sum / ind_count)

    def rand_error(self, ethalon:list=None):
        if ethalon is None:
            self.error('rand_error')
        else:
            for abs in self.mpy_table[ethalon]['abs_error']:
                rand_error = MetroPy.__calc.rounding(abs - self.mpy_table[ethalon]['sys_error'])
                self.mpy_table[ethalon]['rand_error'].append(rand_error)

    def error(self, name_of_error:list):
        for ethalon in self.ethalons:
            eval('self.' + name_of_error + '(ethalon)')

    def visual(self):
        '''mpy_visual = PrettyTable()
        mpy_visual.field_names = self.mpy_table.keys()
        mpy_visual.field_names = self.mpy_table.keys()
        print(mpy_visual)'''
        
        for ethalon in self.mpy_table.keys():
            print(self.mpy_table[ethalon])


user_table = {
    0.5 : [0.579, 0.562, 0.545, 0.566, 0.535, 0.564, 0.558, 0.564, 0.542, 0.544],
    1   : [1.084, 1.084, 1.084, 1.080, 1.074, 1.072, 1.060, 1.080, 1.068, 1.078],
    1.5 : [1.585, 1.576, 1.583, 1.568, 1.570, 1.565, 1.560, 1.570, 1.555, 1.569]
}

mpy = MetroPy(indications=user_table)
mpy.abs_error()
mpy.abs_middle()
mpy.sys_error()
mpy.rand_error()
mpy.dispersion()
mpy.visual()
