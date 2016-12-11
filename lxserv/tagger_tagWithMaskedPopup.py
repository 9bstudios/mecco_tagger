
import lx
import lxifc
import lxu.command
import tagger

CMD_NAME = "tagger.tagWithMaskedPopup"

class ThePopup(lxifc.UIValueHints):
    def __init__(self, items):
        for i in items:
            if i[0] == tagger.MATERIAL:
                self._user = i[1]
            else:
                self._user = "%s (%s)" % (tag[1], tag[0])

        self._internal = ["__".join(i) for i in items]

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._internal)

    def uiv_PopUserName(self,index):
        return self._user[index]

    def uiv_PopInternalName(self,index):
        return self._internal[index]


class TheCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(tagger.QUERY, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add(tagger.SCOPE, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

    def arg_UIValueHints(self, index):
        if index == 0:
            return ThePopup(tagger.items.get_all_masked_tags())
        if index == 1:
            return tagger.PopupClass(tagger.POPUPS_SCOPE)

    def cmd_Execute(self,flags):
        tag = self.dyna_String(0).split("__")
        connected = self.dyna_String(1) if self.dyna_IsSet(1) else tagger.POPUPS_SCOPE[0][0]

        lx.eval('%s %s %s %s' % (tagger.CMD_PTAG_SET, tag[0], tag[1], connected))

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 0:
            va.AddString(tagger.LABEL_TAG_WITH_MASKED)
        return lx.result.OK

lx.bless(TheCommand, CMD_NAME)
