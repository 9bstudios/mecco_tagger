# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_REPLACE
DEFAULTS = [tagger.MATERIAL, '', '']

class CommandClass(lxu.command.BasicCommand):

    _last_used = [None, None, None]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.TAGTYPE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(tagger.REPLACETAG, lx.symbol.sTYPE_STRING)
        self.dyna_Add(tagger.WITHTAG, lx.symbol.sTYPE_STRING)

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

                    if tagType in [tagger.MATERIAL, tagger.PART]:
                        if poly.getTag(tagger.util.string_to_i_POLYTAG(tagType)) == replaceTag:
                            hitlist.add(poly)
                            hitcount += 1

                    elif tagType == tagger.PICK:
                        if not poly.getTag(tagger.util.string_to_i_POLYTAG(tagType)):
                            continue

                        pickTags = set(poly.getTag(tagger.util.string_to_i_POLYTAG(tagType)).split(";"))
                        if replaceTag in pickTags:
                            hitlist.add(poly)
                            hitcount += 1


            with mesh.geometry as geo:
                for poly in hitlist:

                    if tagType in [tagger.MATERIAL, tagger.PART]:
                        poly.setTag(tagger.util.string_to_i_POLYTAG(tagType), withTag)

                    elif tagType == tagger.PICK:
                        pickTags = set(poly.getTag(tagger.util.string_to_i_POLYTAG(tagType)).split(";"))
                        pickTags.discard(replaceTag)
                        pickTags.add(withTag)
                        poly.setTag(tagger.util.string_to_i_POLYTAG(tagType), ";".join(pickTags))


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
            active_layers = tagger.items.get_active_layers()
            polys = []
            if active_layers:
                for layer in active_layers:
                    polys.extend(layer.geometry.polygons.selected)
                if polys:
                    tagType = self.dyna_String(0) if self.dyna_IsSet(0) else DEFAULTS[0]
                    lx.out(polys[0].tags())
                    tag = polys[0].tags()[tagType]
                    self.attr_SetString(1, tag)
                elif not polys:
                    self.attr_SetString(1, DEFAULTS[1])
            elif not active:
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
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

        if index in [1,2]:
            return tagger.PopupClass(tagger.scene.all_tags(x.symbol.i_POLYTAG_MATERIAL))

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_TAGTYPE)

        if index == 1:
            hints.Label(tagger.LABEL_REPLACE_TAG)
            hints.Class ("sPresetText")

        if index == 2:
            hints.Label(tagger.LABEL_WITH_TAG)
            hints.Class ("sPresetText")

lx.bless(CommandClass, CMD_NAME)
