# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = 'tagger.convertTags'

class sPresetText(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items)

    def uiv_PopUserName (self, index):
        return self._items[index]

    def uiv_PopInternalName (self, index):
        return self._items[index]

class CommandClass(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('fromTagType', lx.symbol.sTYPE_STRING)
        self.dyna_Add('toTagType', lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        fromTagType = self.dyna_String(0) if self.dyna_IsSet(0) else 'material'
        toTagType = self.dyna_String(1) if self.dyna_IsSet(1) else 'pick'

        tagger.selection.convert_tags(tagger.util.string_to_i_POLYTAG(fromTagType), tagger.util.string_to_i_POLYTAG(toTagType))

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        return True

    def arg_UIValueHints(self, index):
        if index in [0, 1]:
            return sPresetText(('material', 'part', 'pick'))

    def arg_UIHints (self, index, hints):
        if index in [0, 1]:
            hints.Class ("sPresetText")

lx.bless(CommandClass, CMD_NAME)
