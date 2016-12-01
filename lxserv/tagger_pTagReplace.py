# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = 'tagger.pTagReplace'
DEFAULTS = ['material', '', '']

lookup = {
    'material': lx.symbol.i_POLYTAG_MATERIAL,
    'part': lx.symbol.i_POLYTAG_PART,
    'pick': lx.symbol.i_POLYTAG_PICK
}

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

    _last_used = [None, None, None]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('tagType', lx.symbol.sTYPE_STRING)
        self.dyna_Add('replaceTag', lx.symbol.sTYPE_STRING)
        self.dyna_Add('withTag', lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        tagType = self.dyna_String(0)
        self.set_last_used(0, tagType)

        replaceTag = self.dyna_String(1)
        self.set_last_used(1, replaceTag)

        withTag = self.dyna_String(2)
        self.set_last_used(2, withTag)

        hitcount = 0

        for mesh in modo.Scene().meshes:
            with mesh.geometry as geo:
                hitlist = set()
                for poly in geo.polygons:
                    
                    if tagType in ['material', 'part']:
                        if poly.getTag(lookup[tagType]) == replaceTag:
                            hitlist.add(poly)
                            hitcount += 1

                    elif tagType == 'pick':
                        if not poly.getTag(lookup[tagType]):
                            continue

                        pickTags = set(poly.getTag(lookup[tagType]).split(";"))
                        if replaceTag in pickTags:
                            hitlist.add(poly)
                            hitcount += 1


            with mesh.geometry as geo:
                for poly in hitlist:

                    if tagType in ['material', 'part']:
                        poly.setTag(lookup[tagType], withTag)

                    elif tagType == 'pick':
                        pickTags = set(poly.getTag(lookup[tagType]).split(";"))
                        pickTags.discard(replaceTag)
                        pickTags.add(withTag)
                        poly.setTag(lookup[tagType], ";".join(pickTags))


        if hitcount == 0:
            modo.dialogs.alert("Tag Not Found", "No instances of %s tag '%s' were found in the scene." % (tagType, replaceTag))

        elif hitcount >= 1:
            modo.dialogs.alert("Tag Replaced", "Replaced %s instances of %s tag '%s'." % (hitcount, tagType, replaceTag))

    def cmd_DialogInit(self):
        if self._last_used[0] == None:
            self.attr_SetString(0, DEFAULTS[0])
        else:
            self.attr_SetString(0, self._last_used[0])

        if self._last_used[1] == None:
            self.attr_SetString(1, DEFAULTS[1])
        else:
            self.attr_SetString(1, self._last_used[1])

        if self._last_used[2] == None:
            self.attr_SetString(2, DEFAULTS[2])
        else:
            self.attr_SetString(2, self._last_used[2])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        return True

    def arg_UIValueHints(self, index):
        if index == 0:
            return sPresetText(('material', 'part', 'pick'))

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Class ("sPresetText")

lx.bless(CommandClass, CMD_NAME)
