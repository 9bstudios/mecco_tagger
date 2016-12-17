#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_GROUP

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.NAME,
                    'label': tagger.LABEL_GROUP_NAME,
                    'datatype': 'string',
                    'value': tagger.DEFAULT_GROUP_NAME,
                    'flags': []
                }, {
                    'name': tagger.OPERATION,
                    'label': tagger.LABEL_OPERATION,
                    'datatype': 'string',
                    'value': tagger.ADD,
                    'popup': tagger.POPUPS_ADD_REMOVE,
                    'flags': ['optional']
                }, {
                    'name': tagger.PRESET,
                    'label': tagger.LABEL_PRESET,
                    'datatype': 'string',
                    'value': tagger.RANDOM,
                    'popup': tagger.presets.presets_popup(),
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        group_name = self.commander_arg_value(0)
        operation = self.commander_arg_value(1, tagger.ADD)
        preset = self.commander_arg_value(2, tagger.RANDOM)

        preset = None if preset == tagger.RANDOM else preset

        selmode = tagger.selection.get_mode()

        if operation == tagger.ADD:
            group = tagger.items.group_selected_and_maskable(group_name)
            mask = tagger.shadertree.build_material( group, preset = preset )
            tagger.shadertree.move_to_base_shader(mask)

        if operation == tagger.REMOVE:
            items = tagger.items.get_selected_and_maskable()
            groups = tagger.items.get_groups(selected)
            tagger.shadertree.seek_and_destroy(groups)

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)
        
lx.bless(CommandClass, NAME_CMD)
