#python

import lx, lxu, lxifc, modo, tagger, traceback

NAME = tagger.symbols.ARGS_NAME
MODE = tagger.symbols.ARGS_MODE
OPERATION = tagger.symbols.ARGS_OPERATION
CONNECTED = tagger.symbols.ARGS_CONNECTED
PRESET = tagger.symbols.ARGS_PRESET

AUTO_FILTER = tagger.symbols.FILTER_TYPES_AUTO
MATERIAL = tagger.symbols.FILTER_TYPES_MATERIAL
PART = tagger.symbols.FILTER_TYPES_PART
PICK = tagger.symbols.FILTER_TYPES_PICK

AUTO_OPERATION = tagger.symbols.OPERATIONS_AUTO
ADD = tagger.symbols.OPERATIONS_ADD
REMOVE = tagger.symbols.OPERATIONS_REMOVE

NAME_CMD = tagger.symbols.COMMAND_NAME_PTAG

DEFAULT_TAG = 'Default'

# The UIValueHints object that returns the items in the list of commands
# to the form.
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


class CMD_tagger(lxu.command.BasicCommand):

    _last_used = ''

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME, lx.symbol.sTYPE_STRING)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(CONNECTED, lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(1,5):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_DialogInit(self):
        if self._last_used != '':
            self.attr_SetString(0, self._last_used)
        elif len(tagger.items.get_all_material_tags()) > 0:
            self.attr_SetString(0, tagger.items.get_all_material_tags()[0])

    def arg_UIValueHints(self, index):
        if index == 0:
            return sPresetText(tagger.items.get_all_material_tags())

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Class ("sPresetText")

    @classmethod
    def set_last_used(cls, value):
        cls._last_used = value

    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[NAME] = self.dyna_String(0) if self.dyna_IsSet(0) else DEFAULT_TAG
            args[MODE] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_FILTER
            args[OPERATION] = self.dyna_String(2) if self.dyna_IsSet(2) else AUTO_OPERATION
            args[CONNECTED] = self.dyna_Bool(3) if self.dyna_IsSet(3) else False
            args[PRESET] = self.dyna_String(4) if self.dyna_IsSet(4) else None

            if args[OPERATION] != REMOVE:
                self.set_last_used(args[NAME])

            if args[NAME] == '':
                args[NAME] = DEFAULT_TAG

            if args[MODE] == MATERIAL:
                LXi_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL
            elif args[MODE] == PICK:
                LXi_POLYTAG = lx.symbol.i_POLYTAG_PICK
            else:
                LXi_POLYTAG = lx.symbol.i_POLYTAG_PART

            if args[OPERATION] == AUTO_OPERATION:
                if args[CONNECTED]:
                    tagger.selection.tag_polys( args[NAME], True, LXi_POLYTAG )
                else:
                    tagger.selection.tag_polys( args[NAME], False, LXi_POLYTAG )

                if (
                    not tagger.shadertree.get_masks(pTags = {args[NAME]:LXi_POLYTAG})
                    and not args[NAME] == DEFAULT_TAG
                    ):

                    mask = tagger.shadertree.build_material(
                        i_POLYTAG = LXi_POLYTAG,
                        pTag = args[NAME],
                        preset = args[PRESET]
                    )

                    # tagger.shadertree.cleanup()
                    tagger.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == ADD:
                if args[CONNECTED]:
                    tagger.selection.tag_polys( args[NAME], True, LXi_POLYTAG )
                else:
                    tagger.selection.tag_polys( args[NAME], False, LXi_POLYTAG )

                mask = tagger.shadertree.build_material(
                    i_POLYTAG = LXi_POLYTAG,
                    pTag = args[NAME],
                    preset = args[PRESET]
                )

                # tagger.shadertree.cleanup()
                tagger.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == REMOVE:
                if args[CONNECTED]:
                    tagger.selection.tag_polys( DEFAULT_TAG, True, LXi_POLYTAG )
                else:
                    tagger.selection.tag_polys( DEFAULT_TAG, False, LXi_POLYTAG )

                # tagger.shadertree.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
