
import lx, lxifc, lxu.command, tagger

CMD_NAME = tagger.CMD_PREFS_MATERIAL_TYPE

class CommandClass(tagger.CommanderClass):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.DEFAULT_MATERIAL_TYPE,
                    'label': tagger.LABEL_DEFAULT_MATERIAL_TYPE,
                    'datatype': 'string',
                    'default': tagger.MAT_ADVANCED,
                    'values_list_type': 'popup',
                    'values_list': tagger.POPUPS_MATERIAL_TYPES,
                    'flags': ['query']
                }
            ]

    def commander_execute(self, msg, flags):
        lx.out(tagger.LABEL_DEFAULT_MATERIAL_TYPE, self.commander_arg_value(0))


lx.bless(CommandClass, CMD_NAME)
