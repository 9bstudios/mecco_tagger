# python

import lx, lxifc, lxu, modo
import tagger
from os.path import basename, splitext

CMD_NAME = tagger.CMD_SET_PTAG_PRESET

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.PRESET,
                    'label': tagger.LABEL_PRESET,
                    'datatype': 'string',
                    'value': tagger.RANDOM,
                    'popup': tagger.presets.presets_popup(),
                    'flags': ['query']
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        selmode = tagger.selection.get_mode()

        if selmode == 'item':
            preset = self.commander_arg_value(0, tagger.RANDOM)
            lx.eval("%s %s {%s}" % (tagger.CMD_SET_ITEM, tagger.ADD, preset))

        elif selmode in ['vertex', 'edge', 'polygon']:
            preset = self.commander_arg_value(0, tagger.RANDOM)
            scope = self.commander_arg_value(1, tagger.SCOPE_SELECTED)

            if preset.endswith(".lxp"):
                pTag = splitext(basename(preset))[0]

            elif not preset.endswith(".lxp"):
                pTag = tagger.DEFAULT_MATERIAL_NAME

            lx.eval("%s %s %s %s %s %s" % (tagger.CMD_SET_PTAG, pTag, preset, scope, tagger.MATERIAL, tagger.KEEP))

lx.bless(CommandClass, CMD_NAME)
