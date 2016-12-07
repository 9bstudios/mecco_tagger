# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = 'tagger.convertTags'

class CommandClass(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('fromTagType', lx.symbol.sTYPE_STRING)
        self.dyna_Add('toTagType', lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        fromTagType = self.dyna_String(0) if self.dyna_IsSet(0) else tagger.MATERIAL
        toTagType = self.dyna_String(1) if self.dyna_IsSet(1) else tagger.PICK

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
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Label("From Tag Type")

        if index == 1:
            hints.Label("To Tag Type")

lx.bless(CommandClass, CMD_NAME)
