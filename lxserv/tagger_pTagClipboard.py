#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = 'tagger.pTagClipboard'

class CMD_tagger(lxu.command.BasicCommand):

    _clipboard = {'material': None, 'part': None, 'pick': None}

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.dyna_Add('tagType', lx.symbol.sTYPE_STRING)
        self.dyna_Add('connected', lx.symbol.sTYPE_INTEGER)

        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    @classmethod
    def set_clipboard(cls, key, value):
        cls._clipboard[key] = value

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        mode = self.dyna_String(0) if self.dyna_IsSet(0) else None

        if not mode:
            mode = 'copy'


        tagType = self.dyna_String(1) if self.dyna_IsSet(1) else 'material'
        connected = self.dyna_Int(2) if self.dyna_IsSet(2) else 0


        if mode == 'copy':
            self.set_clipboard(tagType, tagger.selection.get_polys()[0].tags()[tagType])

        elif mode == 'copyMask':
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

            tagLabel = mask.channel(lx.symbol.sICHAN_MASK_PTYP).get()
            tagType = tagger.util.i_POLYTAG_to_string(tagLabel)
            tag = mask.channel(lx.symbol.sICHAN_MASK_PTAG).get()

            self.set_clipboard(tagType, tag)

        elif mode == 'paste':
            args = {}
            args['tag'] = self._clipboard[tagType]
            args['tagType'] = tagType
            args['connected'] = connected

            lx.eval('tagger.pTagSet' + tagger.util.build_arg_string(args))



lx.bless(CMD_tagger, NAME_CMD)
