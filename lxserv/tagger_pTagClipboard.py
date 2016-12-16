#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_PTAG_CLIPBOARD

class CommandClass(tagger.Commander):
    _clipboard = {'material': None, 'part': None, 'pick': None}
    _commander_default_values = []

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

    def basic_Icon(self):
        if self.commander_arg_value(0):
            if self.commander_arg_value(0) == tagger.COPY:
                return 'tagger.copyTags'
            elif self.commander_arg_value(0) == tagger.COPYMASK:
                return 'tagger.copyTags'
            elif self.commander_arg_value(0) == tagger.PASTE and not self.commander_arg_value(1):
                return 'tagger.pasteMaterial'

            elif self.commander_arg_value(0) == tagger.PASTE and self.commander_arg_value(1):
                if self.commander_arg_value(1) == tagger.MATERIAL:
                    return 'tagger.pasteMaterial'
                elif self.commander_arg_value(1) == tagger.PART:
                    return 'tagger.pastePart'
                elif self.commander_arg_value(1) == tagger.PICK:
                    return 'tagger.pasteSet'

        return 'tagger.copyTags'

    def basic_ButtonName(self):
        label = []

        if self.commander_arg_value(0):
            if self.commander_arg_value(0) == tagger.COPY:
                label.append(tagger.LABEL_COPY)
            elif self.commander_arg_value(0) == tagger.COPYMASK:
                label.append(tagger.LABEL_COPY)
            elif self.commander_arg_value(0) == tagger.PASTE:
                label.append(tagger.LABEL_PASTE)
        else:
            label.append(tagger.LABEL_COPY)


        if self.commander_arg_value(0) == tagger.PASTE and self.commander_arg_value(1):
            label.append(tagger.util.i_POLYTAG_to_label(self.commander_arg_value(1)))

        label.append(tagger.LABEL_TAGS)

        if self.commander_arg_value(2):
            if self.commander_arg_value(2) != tagger.SCOPE_SELECTED:
                label.append("(%s)" % self.commander_arg_value(2))

        return " ".join(label)

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
            self.set_clipboard('material', tagger.selection.get_polys()[0].tags()['material'])
            self.set_clipboard('part', tagger.selection.get_polys()[0].tags()['part'])
            self.set_clipboard('pick', tagger.selection.get_polys()[0].tags()['pick'])

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
