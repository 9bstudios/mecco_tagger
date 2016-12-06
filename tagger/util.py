#python

import defaults
from lx import symbol

def random_color():
    import colorsys, random
    return colorsys.hsv_to_rgb(
        random.random(),
        defaults.get('random_color_saturation'),
        defaults.get('random_color_value')
    )

def build_arg_string(arg_dict):
    arg_string = ''
    for k,v in arg_dict.iteritems():
        if v is not None:
            v = str(v) if str(v).isalnum() else '{%s}' % str(v)
            arg_string += " %s:%s" % (str(k),v)
    return arg_string

def string_to_i_POLYTAG(input_string):
    if input_string.lower() == 'material':
        return symbol.i_POLYTAG_MATERIAL
    elif input_string.lower() == 'part':
        return symbol.i_POLYTAG_PART
    elif input_string.lower() in ('pick', 'selection set'):
        return symbol.i_POLYTAG_PICK

def i_POLYTAG_to_string(i_POLYTAG):
    if i_POLYTAG in (symbol.i_POLYTAG_MATERIAL, 'Material'):
        return 'material'
    elif i_POLYTAG in (symbol.i_POLYTAG_PART, 'Part'):
        return 'part'
    elif i_POLYTAG in (symbol.i_POLYTAG_PICK, 'Selection Set'):
        return 'pick'
