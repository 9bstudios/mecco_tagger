# python

import lx, lxifc, lxu, modo
import tagger
from os.path import basename, splitext

CMD_NAME = 'tagger.testArgTypes'

types = [
    # 'ACCELERATION',
    # 'ANGLE',
    'ANGLE3',
    # 'AXIS',
    # 'BOOLEAN',
    'COLOR',
    'COLOR1',
    'DATE',
    'DATETIME',
    # 'DISTANCE',
    'DISTANCE3',
    'FILEPATH',
    # 'FLOAT',
    'FLOAT3',
    # 'FORCE',
    # 'INTEGER',
    # 'LIGHT',
    # 'MASS',
    # 'PERCENT',
    'PERCENT3',
    # 'SPEED',
    # 'STRING',
    'TIME',
    'TOD',
    'UVCOORD',
    'VERTMAPNAME'
]

class CommandClass(tagger.Commander):
    _last_used = []

    def commander_arguments(self):
        args = []
        for t in types:
            args.append({
                'name': t,
                'datatype': t
            })

        return args

    def commander_execute(self, msg, flags):
        for i in range(self.commander_args_count()):
            datatype = type(self.commander_arg_value(i))
            value = self.commander_arg_value(i)
            lx.out("%s: %s" % (datatype, value))

lx.bless(CommandClass, CMD_NAME)
