#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_PTAG_CLIPBOARD

class CMD_tagger(lxu.command.BasicCommand):

    _clipboard = {tagger.MATERIAL: None, tagger.PART: None, tagger.PICK: None}

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.MODE, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.TAGTYPE, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.CONNECTED, lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_MODE)

        if index == 1:
            hints.Label(tagger.LABEL_TAGTYPE)

        if index == 2:
            hints.Label(tagger.LABEL_CONNECTED)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.POPUPS_CLIPBOARD)

        if index == 1:
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

        if index == 2:
            return tagger.PopupClass(tagger.POPUPS_CONNECTED)

    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])
        self.attr_SetString(1, self._last_used[1])
        self.attr_SetInt(2, self._last_used[2])

    @classmethod
    def set_clipboard(cls, key, value):
        cls._clipboard[key] = value

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        mode = self.dyna_String(0) if self.dyna_IsSet(0) else self._last_used[0]
        self.set_last_used(0, mode)

        tagType = self.dyna_String(1) if self.dyna_IsSet(1) else self._last_used[1]
        self.set_last_used(1, tagType)

        connected = self.dyna_String(2) if self.dyna_IsSet(2) else self._last_used[2]
        self.set_last_used(2, connected)

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
            args[tagger.CONNECTED] = connected

            lx.eval(tagger.CMD_PTAG_SET + tagger.util.build_arg_string(args))



lx.bless(CMD_tagger, NAME_CMD)
