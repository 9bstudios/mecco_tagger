# python

import lx
from time import time, strftime
from var import *

_timers = {}

def debug_timer_start(key):
    global _timers
    
    if DEBUG_PERFORMANCE:
        _timers[key] = [0,0]
        _timers[key][0] = time()
    
def debug_timer_end(key):
    global _timers
    
    if DEBUG_PERFORMANCE:
        _timers[key][1] = time()
        elapsed = _timers[key][1] - _timers[key][0]
        lx.out('Timer %.4f (%s)' % ((elapsed * 10), key))