#python

import lx, lxu, modo, traceback

DEBUG = True

try:
    import util
    import defaults
    import items
    import manage
    import shadertree
    import selection
    from var import *
    from PolysConnectedByTag import *
except:
    traceback.print_exc()
