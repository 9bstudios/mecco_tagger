#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_ITEM

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
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
                }, {
                    'name': tagger.WITH_EXISTING,
                    'label': tagger.LABEL_WITH_EXISTING,
                    'datatype': 'string',
                    'value': tagger.POPUPS_WITH_EXISTING[0][0],
                    'popup': tagger.POPUPS_WITH_EXISTING,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        operation = self.commander_arg_value(0)
        preset = self.commander_arg_value(1)
        withExisting = self.commander_arg_value(2)

        if preset == tagger.RANDOM:
            preset = None

        items = tagger.items.get_selected_and_maskable()

        if operation == tagger.ADD:
            for item in items:

                existing_masks = tagger.shadertree.get_masks(item)

                if existing_masks and withExisting == 'use':
                    return

                elif existing_masks and withExisting == 'remove':
                    tagger.shadertree.seek_and_destroy(item)

                elif existing_masks and withExisting == 'consolidate':
                    tagger.shadertree.consolidate(item)

                mask = tagger.shadertree.build_material( item, preset = preset )
                tagger.shadertree.move_to_base_shader(mask)

        if operation == tagger.REMOVE:
            tagger.shadertree.seek_and_destroy(items)


lx.bless(CommandClass, NAME_CMD)
