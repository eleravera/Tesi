#python3 -i 
""" 
"""

import numpy as np
import sys
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def line(x, m ,q):
        return m*x+q
        
def decimal_power(val):
    """Calculate the order of magnitude of a given value,i.e., the largest
    power of ten smaller than the value.
    """
    return int(np.log10(val + sys.float_info.epsilon)) - 1 * (val < 1.)
            
def decimal_places(val):
    """Calculate the number of decimal places so that a given value is rounded
    to exactly two signficant digits.
    Note that we add epsilon to the argument of the logarithm in such a way
    that, e.g., 0.001 is converted to 0.0010 and not 0.00100. For values greater
    than 99 this number is negative.
    """
    return 1 - int(np.log10(val + sys.float_info.epsilon)) + 1 * (val < 1.)        
        
def format_value_error(value, error, pm='+/-', max_dec_places=6):
    """Format a measurement with the proper number of significant digits.
    """
    value = float(value)
    error = float(error)
    if not np.isnan(error):
        assert error >= 0
    else:
        return '%s %s nan' % (format_value(value), pm)
    if error == 0 or error == np.inf:
        return '%e' % value
    dec_places = decimal_places(error)
    if dec_places >= 0 and dec_places <= max_dec_places:
        fmt = '%%.%df %s %%.%df' % (dec_places, pm, dec_places)
    else:
        p = decimal_power(abs(value))
        scale = 10 ** p
        value /= scale
        error /= scale
        dec_places = decimal_places(error)
        if dec_places > 0:
            if p > 0:
                exp = 'e+%02d' % p
            else:
                exp = 'e-%02d' % abs(p)
            fmt = '%%.%df%s %s %%.%df%s' %\
                  (dec_places, exp, pm, dec_places, exp)
        else:
            fmt = '%%d %s %%d' % pm
    return fmt % (value, error)
        



dict_file_parameters = {'START FREEZE = 50': '/home/eleonora/tesi/Tesi/data/dead_time/CONF_START_FREEZE_50.txt', 
            'START READ = 60' : '/home/eleonora/tesi/Tesi/data/dead_time/CONF_START_READ_60.txt',
            'START READ = 68' : '/home/eleonora/tesi/Tesi/data/dead_time/CONF_START_READ_68.txt',
            'STOP FREEZE = 95' : '/home/eleonora/tesi/Tesi/data/dead_time/CONF_STOP_FREEZE_95.txt',
            'STOP FREEZE = 105' : '/home/eleonora/tesi/Tesi/data/dead_time/CONF_STOP_FREEZE_105.txt',
            'STOP READ = 80' : '/home/eleonora/tesi/Tesi/data/dead_time/CONF_STOP_READ_80.txt', 
            'DEFAULT' : '/home/eleonora/tesi/Tesi/data/dead_time/default_cols_q40.txt'
             }
             
dict_file_DEFAULT = {'ROWS, Q = 40 DAC': '/home/eleonora/tesi/Tesi/data/dead_time/default_rows.txt',  
                     'COLUMNS, Q = 40 DAC' : '/home/eleonora/tesi/Tesi/data/dead_time/default_cols_q40.txt',
                     'COLUMNS, Q = 80 DAC' : '/home/eleonora/tesi/Tesi/data/dead_time/default_cols_q80.txt'
             }
             
             
             
fmts_points = ['or', '^b', 'vg', '*k', 'sc', 'Dm', 'xy']
fmts_lines = ['--r', '--b', '--g', '--k', '--c', '--m', '--y']
param_names = ['m', 'q']
param_units =['clk units/pix', 'clk units']

fig, ax = plt.subplots(1,1, figsize=(8, 8))
ax.set_xlabel("N of pixels", fontsize=14)
ax.set_ylabel("R/O time [clk cnts]", fontsize=14)
range_pixels = (0, 250)
range_tau = (0, 1.e+4)
ax.set_xbound(range_pixels)
ax.set_ybound(range_tau)
ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)
ax2 = ax.twinx()

#fign, axn = plt.subplots(1,1, figsize=(8, 8))
#axn.set_xlabel("N of pixels", fontsize=14)
#axn.set_ylabel("R/O time / pixel [clk cnts/pix]", fontsize=14)
#axn.set_xbound(range_pixels)
#axn.set_ybound((0.5, 2.))
#axn.xaxis.set_tick_params(labelsize=14)
#axn.yaxis.set_tick_params(labelsize=14)


for key, fmt_p, fmt_l in zip(dict_file_DEFAULT, fmts_points, fmts_lines):
        #print(key)
        data = np.transpose(np.loadtxt(dict_file_DEFAULT[key]))
        legend = key               
        #axn.errorbar(data[0], data[1]/data[0], yerr = data[2]/data[0], fmt = fmt_p, ms=7, label = legend)        
        #axn.legend()
        
        data[1] = data[1]  
        data[2] = data[2] 
        legend = legend + ':\n'                
        opt, pcov = curve_fit(line, data[0], data[1], sigma = data[2], absolute_sigma = True)
        for (name, value, error, unit) in zip(param_names, opt, np.sqrt(pcov.diagonal()), param_units):
                legend += ("    %s: %s %s\n" % (name, format_value_error(value, error), unit))   
        
        data[1] = data[1] * 25 * 1.e-3 
        data[2] = data[2] * 25 * 1.e-3 
        opt, pcov = curve_fit(line, data[0], data[1], sigma = data[2], absolute_sigma = True)
        ax2.errorbar(data[0], data[1], yerr = data[2], fmt = fmt_p, ms=7, label = legend)
        x = np.linspace(0, data[0].max(), 1000)
        ax2.plot(x, line(x, *opt), fmt_l)
        ax2.legend()
        
        
#ax2.set_ylabel("R/O time [us]", fontsize=14)
#range_tau_us = (0, 10 * 25)
#ax2.set_ybound(range_tau_us)
#ax2.yaxis.set_tick_params(labelsize=14)
#ax2.set_xbound(range_pixels)
        
plt.show()
