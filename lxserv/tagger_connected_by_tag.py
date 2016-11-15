# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = 'tagger.selectConnectedByTag'

def search_neighbors(poly, pTagType = 'material', pTags = set(), snowball = set()):

    if len(snowball) == 0:
        if not pTags:
            pTags = pTags.union(set(poly.tags()[pTagType].split(";")))

    for neighbor in [p for p in poly.neighbours if p not in snowball]:
        if neighbor.tags()[pTagType] not in pTags:
            continue

        snowball.add(neighbor)
        snowball.union(search_neighbors(neighbor, pTagType, pTags, snowball))

    return snowball

class sPresetText(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items)

    def uiv_PopUserName (self, index):
        return self._items[index][1]

    def uiv_PopInternalName (self, index):
        return self._items[index][0]

class myGreatCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('tagType', lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        tagType = self.dyna_String(0) if self.dyna_IsSet(0) else None
        for poly in tagger.selection.get_polys(False):
            connected = search_neighbors(poly, tagType)
            for p in connected:
                p.select()

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        return True

    def arg_UIValueHints(self, index):
        if index == 0:
            return sPresetText((('material', 'Material'), ('part', 'Part'), ('pick', 'Selection Set')))

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Class ("sPresetText")

lx.bless(myGreatCommand, CMD_NAME)
