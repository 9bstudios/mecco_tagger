
import lx
import lxifc
import lxu.command
import tagger

CMD_NAME = "tagger.tagWithMaskedPopup"

class ThePopup(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items)

    def uiv_PopUserName(self,index):
        return self._items[index]

    def uiv_PopInternalName(self,index):
        return self._items[index]


class TheCommand(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('masks', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add('connected', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)


    def arg_UIValueHints(self, index):
        if index == 0:
            return ThePopup(tagger.items.get_all_material_tags())

    def cmd_Execute(self,flags):
        connected = self.dyna_Int(1) if self.dyna_IsSet(1) else 0
        if self.dyna_IsSet(0):
            lx.eval('tagger.pTagSet material %s %s' % (self.dyna_String(0), connected))

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 0:
            va.AddString("Tag With Masked...")
        return lx.result.OK

lx.bless(TheCommand, CMD_NAME)
