# python

import lx, lxu, modo, tagger, traceback

NAME_CMD = 'tagger.tagWithMasked'

class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.CONNECTED, lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        connected = self.dyna_Int(0) if self.dyna_IsSet(0) else 0
        masks = set()

        for i in modo.Scene().selected:
            if i.type == 'mask':
                masks.add(i)

        if len(masks) < 1:
            modo.dialogs.alert("No Mask Selected", "Select a mask to apply.")
            return

        if len(masks) > 1:
            modo.dialogs.alert("Too Many Masks", "Select only one mask to apply.")
            return

        mask = list(masks)[0]

        if not mask.channel(lx.symbol.sICHAN_MASK_PTAG).get():
            modo.dialogs.alert("No pTag Filter", "The selected mask applies to all polygons. No tag to apply.")
            return

        if mask.channel(lx.symbol.sICHAN_MASK_PTAG).get() == "(none)":
            modo.dialogs.alert("(none) pTag Filter", "The selected mask applies to nothing. No tag to apply.")
            return

        tagLabel = mask.channel(lx.symbol.sICHAN_MASK_PTYP).get()
        tag = mask.channel(lx.symbol.sICHAN_MASK_PTAG).get()

        tagger.selection.tag_polys(tag, connected, tagger.util.string_to_i_POLYTAG(tagLabel))

lx.bless(CMD_tagger, NAME_CMD)
