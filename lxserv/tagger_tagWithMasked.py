# python

import lx, lxu, modo, tagger, traceback

NAME_CMD = 'tagger.tagWithMasked'

lookup = {
    'Material': lx.symbol.i_POLYTAG_MATERIAL,
    'Part': lx.symbol.i_POLYTAG_PART,
    'Selection Set': lx.symbol.i_POLYTAG_PICK
}

class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
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

        tagger.selection.tag_polys(tag, False, lookup[tagLabel])

lx.bless(CMD_tagger, NAME_CMD)
