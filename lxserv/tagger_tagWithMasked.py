# python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_TAG_WITH_MASKED

class CMD_tagger(lxu.command.BasicCommand):
    _last_used = [
        tagger.POPUPS_SCOPE[0][0]
    ]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.SCOPE, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_SCOPE)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.POPUPS_SCOPE)

    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        connected = self.dyna_String(0) if self.dyna_IsSet(0) else self._last_used[0]
        self.set_last_used(0, connected)

        masks = set()

        for i in modo.Scene().selected:
            if i.type == 'mask':
                masks.add(i)

        if len(masks) < 1:
            modo.dialogs.alert(tagger.DIALOGS_NO_MASK_SELECTED)
            return

        if len(masks) > 1:
            modo.dialogs.alert(tagger.DIALOGS_TOO_MANY_MASKS)
            return

        mask = list(masks)[0]

        if not mask.channel(lx.symbol.sICHAN_MASK_PTAG).get():
            modo.dialogs.alert(tagger.DIALOGS_NO_PTAG_FILTER)
            return

        if mask.channel(lx.symbol.sICHAN_MASK_PTAG).get() == "(none)":
            modo.dialogs.alert(tagger.DIALOGS_NONE_PTAG_FILTER)
            return

        tagLabel = mask.channel(lx.symbol.sICHAN_MASK_PTYP).get()
        tag = mask.channel(lx.symbol.sICHAN_MASK_PTAG).get()

        tagger.selection.tag_polys(tag, connected, tagger.util.string_to_i_POLYTAG(tagLabel))

lx.bless(CMD_tagger, NAME_CMD)
