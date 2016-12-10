# python

import lx, lxifc, lxu, modo
import tagger
from os import listdir, sep
from os.path import isfile, join, basename, splitext, dirname

CMD_NAME = tagger.CMD_SET_PTAG

class CommandClass(lxu.command.BasicCommand):
    _last_used = [
        "",
        tagger.RANDOM,
        tagger.POPUPS_CONNECTED[2][0],
        tagger.POPUPS_TAGTYPES[0][0],
        tagger.POPUPS_WITH_EXISTING[0][0]
    ]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.TAG, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.PRESET, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_QUERY)

        self.dyna_Add(tagger.CONNECTED, lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.TAGTYPE, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.WITH_EXISTING, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(4, lx.symbol.fCMDARG_OPTIONAL)

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

        if index == 4:
            hints.Label(tagger.LABEL_WITH_EXISTING)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL))

        if index == 1:
            popup_list = [(tagger.RANDOM, tagger.LABEL_RANDOM_COLOR)]
            popup_list.extend(tagger.presets.list_presets())
            return tagger.PopupClass(popup_list)

        if index == 2:
            return tagger.PopupClass(tagger.POPUPS_CONNECTED)

        if index == 3:
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

        if index == 4:
            return tagger.PopupClass(tagger.POPUPS_WITH_EXISTING)

    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])
        self.attr_SetString(1, self._last_used[1])
        self.attr_SetInt(2, self._last_used[2])
        self.attr_SetString(3, self._last_used[3])
        self.attr_SetString(4, self._last_used[4])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        pTag = self.dyna_String(0) if self.dyna_IsSet(0) else ''
        self.set_last_used(0, pTag)

        preset = self.dyna_String(1)
        self.set_last_used(1, preset)
        preset = None if preset == tagger.RANDOM else preset

        connected = self.dyna_Int(2) if self.dyna_IsSet(2) else self._last_used[2]
        self.set_last_used(2, connected)

        tagType = self.dyna_String(3) if self.dyna_IsSet(3) else self._last_used[3]
        self.set_last_used(3, tagType)
        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

        withExisting = self.dyna_String(4) if self.dyna_IsSet(4) else self._last_used[4]
        self.set_last_used(4, withExisting)

        if not pTag and (not preset or not preset.endswith(".lxp")):
            pTag = tagger.DEFAULT_MATERIAL_NAME

        elif not pTag and preset.endswith(".lxp"):
            pTag = splitext(basename(preset))[0]

        # find any existing masks for this pTag
        existing_masks = tagger.shadertree.get_masks( pTags = { pTag: i_POLYTAG })

        # tag the polys
        tagger.selection.tag_polys(pTag, connected, i_POLYTAG)

        # build a new mask if we need one
        if not existing_masks or (existing_masks and withExisting != tagger.POPUPS_WITH_EXISTING[0][0]):
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag, preset = preset)

        if existing_masks and withExisting == tagger.POPUPS_WITH_EXISTING[1][0]:
            tagger.util.safe_removeItems(existing_masks, True)

        elif existing_masks and withExisting == tagger.POPUPS_WITH_EXISTING[2][0]:
            tagger.shadertree.consolidate(pTags = { pTag: i_POLYTAG })


    def cmd_Query(self,index,vaQuery):
        pass
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 1:
            va.AddString(self._last_used[1])

        return lx.result.OK


lx.bless(CommandClass, CMD_NAME)
