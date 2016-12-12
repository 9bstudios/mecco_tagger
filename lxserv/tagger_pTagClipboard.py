#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_PTAG_CLIPBOARD

class CommandClass(tagger.Commander):
    _clipboard = {tagger.MATERIAL: None, tagger.PART: None, tagger.PICK: None}
    _commander_last_used = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.MODE,
                    'label': tagger.LABEL_MODE,
                    'datatype': 'string',
                    'value': tagger.COPY,
                    'popup': tagger.POPUPS_CLIPBOARD,
                    'flags': ['optional'],
                }, {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': ['optional']
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }
            ]

    @classmethod
    def set_clipboard(cls, key, value):
        cls._clipboard[key] = value

    def commander_execute(self, msg, flags):
        mode = self.commander_arg_value(0)
        tagType = self.commander_arg_value(1)
        connected = self.commander_arg_value(2)

        if not mode:
            mode = tagger.COPY

        if mode == tagger.COPY:
            self.set_clipboard(tagType, tagger.selection.get_polys()[0].tags()[tagType])

        elif mode == tagger.COPYMASK:
            masks = set()

            for i in modo.Scene().selected:
                if i.type == tagger.MASK:
                    masks.add(i)

            if len(masks) < 1:
                modo.dialogs.alert(tagger.DIALOGS_NO_MASK_SELECTED)
                return

            if len(masks) > 1:
                modo.dialogs.alert(tagger.DIALOGS_TOO_MANY_MASKS)
                return

            mask = list(masks)[0]

            tagLabel = mask.channel(lx.symbol.sICHAN_MASK_PTYP).get()
            tagType = tagger.util.i_POLYTAG_to_string(tagLabel)
            tag = mask.channel(lx.symbol.sICHAN_MASK_PTAG).get()

            self.set_clipboard(tagType, tag)

        elif mode == tagger.PASTE:
            args = {}
            args[tagger.TAG] = self._clipboard[tagType]
            args[tagger.TAGTYPE] = tagType
            args[tagger.SCOPE] = connected

            lx.eval(tagger.CMD_PTAG_SET + tagger.util.build_arg_string(args))


lx.bless(CommandClass, NAME_CMD)
