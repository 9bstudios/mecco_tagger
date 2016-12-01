# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = 'tagger.pTagRemoveAll'
DEFAULTS = ['part', '', False]

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

    _last_used = [None]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('tagType', lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        tagType = self.dyna_String(0) if self.dyna_IsSet(0) else 'material'
        self.set_last_used(0, tagType)

        safety = modo.dialogs.yesNo("Remove All Tags", "All %s tags will be removed from the scene. Continue?" % tagType)

        if safety == 'yes':
            for mesh in modo.Scene().meshes:
                with mesh.geometry as geo:
                    polys = geo.polygons
                    tagger.manage.tag_polys(polys, None, lookup[tagType])

    def cmd_DialogInit(self):
        if self._last_used[0] == None:
            self.attr_SetString(0, DEFAULTS[0])
        else:
            self.attr_SetString(0, self._last_used[0])

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
