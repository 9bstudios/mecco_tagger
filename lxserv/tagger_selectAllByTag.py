# python

import lx, lxu, lxifc, modo, tagger, traceback

NAME_CMD = tagger.CMD_SELECT_ALL_BY_TAG

class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add (tagger.TAGTYPE, lx.symbol.sTYPE_STRING)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Class ("sPresetText")

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        tagType = self.dyna_String(0) if self.dyna_IsSet(0) else tagger.MATERIAL

        tags = set()
        for p in tagger.selection.get_polys():
            tag = p.tags()[tagType]
            if tag:
                tag = tag.split(";")
            if not tag:
                tag = []
            tags.update(tag)

        for tag in tags:
            lx.eval("select.polygon add %s face %s" % (tagType, tag))


lx.bless(CMD_tagger, NAME_CMD)
