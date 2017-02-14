
import lx, lxifc, lxu.command, tagger, modo

CMD_NAME = tagger.CMD_PREFS_MATERIAL_TYPE

def material_types_list():
    types = [
            (tagger.MAT_ADVANCED, tagger.LABEL_MAT_ADVANCED),
            (tagger.MAT_UNREAL, tagger.LABEL_MAT_UNREAL),
            (tagger.MAT_UNITY, tagger.LABEL_MAT_UNITY)
        ]

    valid_types = []

    for material_type in types:
        try:
            modo.Scene().items(material_type[0])
            valid_types.append(material_type)
        except LookupError:
            continue

    return valid_types

class CommandClass(tagger.CommanderClass):
    # _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.DEFAULT_MATERIAL_TYPE,
                    'label': tagger.LABEL_DEFAULT_MATERIAL_TYPE,
                    'datatype': 'string',
                    'default': lx.eval("user.value mecco_tagger.materialType ?"),
                    'values_list_type': 'popup',
                    'values_list': material_types_list,
                    'flags': ['query']
                }
            ]

    def commander_execute(self, msg, flags):
        lx.eval("user.value mecco_tagger.materialType %s" % self.commander_arg_value(0))
        lx.out(tagger.LABEL_DEFAULT_MATERIAL_TYPE, "-", self.commander_arg_value(0))


lx.bless(CommandClass, CMD_NAME)
