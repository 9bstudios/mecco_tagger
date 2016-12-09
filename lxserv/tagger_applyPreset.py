# python

import lx, lxifc, lxu, modo
import tagger

CMD_NAME = tagger.CMD_APPLY_PRESET

class CommandClass(lxu.command.BasicCommand):
    _last_used = ["", tagger.RANDOM, 2, tagger.MATERIAL]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.TAG, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add(tagger.PRESET, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add(tagger.CONNECTED, lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.TAGTYPE, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

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

        if index == 3:
            hints.Label(tagger.LABEL_TAGTYPE)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL))

        if index == 1:
            popup_list = [(tagger.RANDOM, tagger.LABEL_RANDOM_COLOR)]
            popup_list.extend(tagger.presets.list_presets())
            popup_list.extend([(tagger.GET_MORE_PRESETS, tagger.LABEL_GET_MORE_PRESETS)])
            return tagger.PopupClass(popup_list)

        if index == 2:
            return tagger.PopupClass(tagger.POPUPS_CONNECTED)

        if index == 3:
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])
        self.attr_SetString(1, self._last_used[1])
        self.attr_SetInt(2, self._last_used[2])
        self.attr_SetString(3, self._last_used[3])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        tag = self.dyna_String(0)
        self.set_last_used(0, tag)

        preset = self.dyna_String(1)
        self.set_last_used(1, preset)

        connected = self.dyna_Int(2) if self.dyna_IsSet(2) else self._last_used[2]
        self.set_last_used(2, self.dyna_Int(2))

        tagType = self.dyna_Int(3) if self.dyna_IsSet(3) else self._last_used[3]
        self.set_last_used(3, self.dyna_Int(3))

        if preset == tagger.GET_MORE_PRESETS:
            lx.eval('openURL {%s}' % tagger.GET_MORE_PRESETS_URL)
            return

        if preset == tagger.RANDOM:
            preset = None

        tagger.selection.tag_polys(tag, connected, lx.symbol.i_POLYTAG_MATERIAL)
        tagger.shadertree.build_material(
                item = None,
                i_POLYTAG = tagger.string_to_i_POLYTAG(tagType),
                pTag = tag,
                parent = None,
                name = None,
                preset = preset,
                shader = False
                )

    def cmd_Query(self,index,vaQuery):
        pass
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 1:
            va.AddString(self._last_used[1])

        return lx.result.OK


lx.bless(CommandClass, CMD_NAME)
