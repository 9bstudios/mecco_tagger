# python

import lx, lxifc, lxu, modo
import tagger
from os import listdir, sep
from os.path import isfile, join, basename, splitext, dirname

CMD_NAME = tagger.CMD_REMOVE_PTAG

class CommandClass(lxu.command.BasicCommand):
    _last_used = [
        tagger.POPUPS_TAGTYPES[0][0],
        tagger.POPUPS_REMOVE_SCOPE[2][0],
        True
    ]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.TAGTYPE, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.REMOVE_SCOPE, lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.DELETE_UNUSED_MASKS, lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_TAGTYPE)

        if index == 1:
            hints.Label(tagger.LABEL_REMOVE_SCOPE)

        if index == 2:
            hints.Label(tagger.LABEL_DELETE_UNUSED_MASKS)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

        if index == 1:
            return tagger.PopupClass(tagger.POPUPS_REMOVE_SCOPE)

    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])
        self.attr_SetString(1, self._last_used[1])
        self.attr_SetString(2, self._last_used[2])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        tagType = self.dyna_String(0) if self.dyna_IsSet(0) else self._last_used[0]
        self.set_last_used(0, self.dyna_Int(0))
        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

        scope = self.dyna_Int(1) if self.dyna_IsSet(1) else self._last_used[1]
        self.set_last_used(1, self.dyna_Int(1))

        delete_unused = self.dyna_Int(2) if self.dyna_IsSet(2) else self._last_used[2]
        self.set_last_used(2, self.dyna_Int(2))

        pTags_to_remove = tagger.selection.get_ptags(i_POLYTAG)

        # if we're just nixing tags in a selection, easy.
        if scope in [0,1,2]:
            tagger.selection.tag_polys(None, scope, i_POLYTAG)

        # if we want to nix tags for the whole scene, do some work.
        if scope == 3:
            for  pTag in pTags_to_remove:
                lx.eval("%s %s %s {}" % (tagger.CMD_PTAG_REPLACE, tagType, pTag))

        # see if we need to delete any masks in the shader tree
        if not delete_unused:
            return

        mask_tags_to_destroy = set()
        for pTag in pTags_to_remove:
            if not tagger.scene.meshes_with_pTag(pTag, i_POLYTAG):
                tagger.shadertree.seek_and_destroy(pTags={pTag:i_POLYTAG})


lx.bless(CommandClass, CMD_NAME)
