import numpy as np

def create_comp_string(gas, options):
    x = options.comp
    final_string = ''

    for idx, compound in enumerate(options.palette):
        final_string += compound + ":" + str(x[idx])
        if idx != len(x)-1:
            final_string += ","

    return final_string

def set_gas_using_palette(gas, options):
    comp_string = create_comp_string(gas, options)
    gas.TPX = options.temp, options.pres, comp_string
    return comp_string

def readable(action):
    if (action == 2):
	return "INCREASE"
    elif (action == 1):
	return "SAME"
    elif (action == 0):
	return "DECREASE"

