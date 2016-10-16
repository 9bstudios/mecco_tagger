#python

import modo, lx, lxu, symbols

DEFAULTS = {
    "ptag": 'Default',
    "name": 'untitled',
    "random_color_saturation": .7,
    "random_color_value": .95,
    "base_material_color": (.8,.8,.8),
    "mask_filter": lx.symbol.i_POLYTAG_MATERIAL,
    'material_channels':{
        lx.symbol.sICHAN_ADVANCEDMATERIAL_DIFFAMT: 0.8,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_DIFFCOL: None,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_SPECAMT: 0.04,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_SMOOTH: True,
        lx.symbol.sICHAN_ADVANCEDMATERIAL_DBLSIDED: True
    },
    'shader_channels':{
        lx.symbol.sICHAN_DEFAULTSHADER_SHADERATE: 0.25,
    },
    'environment_channels':{
        lx.symbol.sICHAN_ENVIRONMENT_VISCAM: True,
        lx.symbol.sICHAN_ENVIRONMENT_VISIND: True,
        lx.symbol.sICHAN_ENVIRONMENT_VISREFL: True,
        lx.symbol.sICHAN_ENVIRONMENT_VISREFR: True,
        lx.symbol.sICHAN_ENVIRONMENT_RADIANCE: 1.0,
    },
    "default": False,
    "useLib": False,
}

def get(key):
    """Returns a default value for a given key."""
    return DEFAULTS[key]


def merge(overrides={},defaults=DEFAULTS):
    """Merges two objects recursively such that any elements existing in
    'overrides' are retained, and any missing elements will be replaced
    with those in 'defaults'. Useful for things like material channels,
    where the UI design may need to customize a specific channel, while
    leaving the rest at their default values.

    :param overrides: object containing override values
    :param defaults: object containing default values
    """

    result = defaults

    if isinstance(overrides,dict):
        for k,v in defaults.iteritems():
            if isinstance(v,list) or isinstance(v,dict) or isinstance (v,tuple):
                result[k] = merge(v,defaults[k])
            else:
                result[k] = overrides.get(k,result[k])

        for k,v in overrides.iteritems():
            if not hasattr(result,k):
                result[k] = v

    elif isinstance(overrides,list):
        for i in range(len(defaults)):
            try:
                result[i] = overrides[i]
            except:
                result[i] = defaults[i]

        for i in range(len(result),len(overrides)):
            result[i] = overrides[i]

    elif isinstance(overrides,tuple):
        result = overrides

    return result
