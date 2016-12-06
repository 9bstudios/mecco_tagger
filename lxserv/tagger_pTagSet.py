# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = 'tagger.pTagSet'
DEFAULTS = ['material', '', False]

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
        self.dyna_Add('tag', lx.symbol.sTYPE_STRING)
        self.dyna_Add('connected', lx.symbol.sTYPE_INTEGER)

        for i in [1,2]:
            self.basic_SetFlags (i, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        tagType = self.dyna_String(0) if self.dyna_IsSet(0) else 'material'
        self.set_last_used(0, tagType)

        tag = self.dyna_String(1) if self.dyna_IsSet(1) else None
        self.set_last_used(1, tag)

        connected = self.dyna_Int(2) if self.dyna_IsSet(2) else 0
        self.set_last_used(2, connected)

        tagger.selection.tag_polys(tag, connected, tagger.util.string_to_i_POLYTAG(tagType))

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
            self.attr_SetInt(2, DEFAULTS[2])
        else:
            self.attr_SetInt(2, self._last_used[2])

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

    def basic_ButtonName(self):
        if self.dyna_IsSet(0) and self.dyna_IsSet(1):
            tagType = self.dyna_String(0)
            tag = self.dyna_String(1)
            return "%s (%s)" % (tag, tagType)

    def arg_UIValueHints(self, index):
        if index == 0:
            return sPresetText(('material', 'part', 'pick'))

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Class ("sPresetText")

lx.bless(CommandClass, CMD_NAME)
