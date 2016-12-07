# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_REMOVEALL
DEFAULTS = [tagger.PART, '', False]

class CommandClass(lxu.command.BasicCommand):

    _last_used = [None]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.TAGTYPE, lx.symbol.sTYPE_STRING)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        tagType = self.dyna_String(0) if self.dyna_IsSet(0) else tagger.MATERIAL
        self.set_last_used(0, tagType)

        safety = modo.dialogs.yesNo("Remove All Tags", "All %s tags will be removed from the scene. Continue?" % tagType)

        if safety == 'yes':
            for mesh in modo.Scene().meshes:
                with mesh.geometry as geo:
                    polys = geo.polygons
                    tagger.manage.tag_polys(polys, None, tagger.util.string_to_i_POLYTAG(tagType))

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
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_TAGTYPE)

lx.bless(CommandClass, CMD_NAME)
