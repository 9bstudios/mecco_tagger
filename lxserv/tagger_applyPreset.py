# python

import lx, lxifc, lxu, modo
import tagger

CMD_NAME = tagger.CMD_APPLY_PRESET

class CommandClass(lxu.command.BasicCommand):
    _last_used = ["", tagger.presets.list_presets()[0][0], 2]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.TAG, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add(tagger.PRESET, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add(tagger.CONNECTED, lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_TAG)
            hints.Class("sPresetText")

        if index == 1:
            hints.Label(tagger.LABEL_PRESET)

        if index == 2:
            hints.Label(tagger.LABEL_CONNECTED)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL))

        if index == 1:
            return tagger.PopupClass(tagger.presets.list_presets())

        if index == 2:
            return tagger.PopupClass(tagger.POPUPS_CONNECTED)

    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])
        self.attr_SetString(1, self._last_used[1])
        self.attr_SetInt(2, self._last_used[2])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        if self.dyna_IsSet(0):
            lx.out(self.dyna_String(0))
            self.set_last_used(0, self.dyna_String(0))

        if self.dyna_IsSet(1):
            lx.out(self.dyna_String(1))
            self.set_last_used(1, self.dyna_String(1))

        if self.dyna_IsSet(2):
            lx.out(self.dyna_Int(2))
            self.set_last_used(2, self.dyna_Int(2))

    def cmd_Query(self,index,vaQuery):
        pass
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 1:
            va.AddString(tagger.presets.list_presets()[0][0])

        return lx.result.OK


lx.bless(CommandClass, CMD_NAME)
