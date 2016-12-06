
import lx
import lxifc
import lxu.command
import tagger

CMD_NAME = "tagger.tagWithMaskedPopup"

class ThePopup(lxifc.UIValueHints):
    def __init__(self, items):
        # Weird hack. uiv_PopInternalName() was inexplicably returning
        # unrelated method names (as strings?) when I tried to concatenate
        # these tuples there. To get around it, I combine them into a single
        # string here, then split them back out for the pretty print.
        self._items = ["__".join(i) for i in items]

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items)

    def uiv_PopUserName(self,index):
        tag = self._items[index].split("__")
        if tag[0] == 'material':
            return tag[1]
        else:
            return "%s (%s)" % (tag[1], tag[0])

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
            return ThePopup(tagger.items.get_all_masked_tags())

    def cmd_Execute(self,flags):
        tag = self.dyna_String(0).split("__")
        connected = self.dyna_Int(1) if self.dyna_IsSet(1) else 0

        lx.eval('tagger.pTagSet %s %s %s' % (tag[0], tag[1], connected))

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 0:
            va.AddString("Tag With Masked...")
        return lx.result.OK

lx.bless(TheCommand, CMD_NAME)
