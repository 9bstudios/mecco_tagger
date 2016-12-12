#python

from lx import symbol
from var import *

def random_color():
    import colorsys, random
    return colorsys.hsv_to_rgb(
        random.random(),
        DEFAULT_RANDOM_COLOR_SATURATION,
        DEFAULT_RANDOM_COLOR_VALUE
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

def i_POLYTAG_to_label(i_POLYTAG):
    if i_POLYTAG in (symbol.i_POLYTAG_MATERIAL, 'Material', 'material'):
        return LABEL_MATERIAL
    elif i_POLYTAG in (symbol.i_POLYTAG_PART, 'Part', 'part'):
        return LABEL_PART
    elif i_POLYTAG in (symbol.i_POLYTAG_PICK, 'Selection Set', 'pick'):
        return LABEL_PICK

def sICHAN_MASK_PTYP(string_or_int):
    if string_or_int in (symbol.i_POLYTAG_MATERIAL, 'material'):
        return 'Material'
    elif string_or_int in (symbol.i_POLYTAG_PART, 'part'):
        return 'Part'
    elif string_or_int in (symbol.i_POLYTAG_PICK, 'pick'):
        return 'Selection Set'

def safe_removeItems(items, children = False):
    for i in items:

        # make sure item exists before trying to delete it
        # (lest ye crash)
        try:
            modo.Scene().item(i.id)
        except:
            continue

        modo.Scene().removeItems(i, children)
