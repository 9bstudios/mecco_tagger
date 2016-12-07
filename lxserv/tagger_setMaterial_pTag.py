#python

import lx, lxu, lxifc, modo, tagger, traceback

NAME = tagger.NAME
MODE = tagger.MODE
OPERATION = tagger.OPERATION
CONNECTED = tagger.CONNECTED
PRESET = tagger.PRESET

AUTO_FILTER = tagger.FILTER_TYPES_AUTO
MATERIAL = tagger.FILTER_TYPES_MATERIAL
PART = tagger.FILTER_TYPES_PART
PICK = tagger.FILTER_TYPES_PICK

AUTO_OPERATION = tagger.OPERATIONS_AUTO
ADD = tagger.OPERATIONS_ADD
REMOVE = tagger.OPERATIONS_REMOVE

NAME_CMD = tagger.CMD_SET_PTAG

DEFAULT_TAG = ''

class CMD_tagger(lxu.command.BasicCommand):

    _last_used = ''
    _last_used_mode = tagger.MATERIAL

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME, lx.symbol.sTYPE_STRING)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(CONNECTED, lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        for i in range(2,5):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_DialogInit(self):
        if self._last_used != '':
            self.attr_SetString(0, self._last_used)
        elif len(tagger.items.get_all_masked_tags()) > 0:
            self.attr_SetString(0, tagger.items.get_all_masked_tags()[0][1])

        self.attr_SetString(1, self._last_used_mode)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL))

        if index == 1:
            return tagger.PopupClass(tagger.POPUPS_TAGTYPES)

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Class("sPresetText")
            hints.Label("Tag")

        if index == 1:
            hints.Label(tagger.LABEL_TAGTYPE)

    @classmethod
    def set_last_used(cls, value):
        cls._last_used = value

    @classmethod
    def set_last_used_mode(cls, value):
        cls._last_used_mode = value

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

            self.set_last_used_mode(args[NAME])

            if args[NAME] == '':
                args[NAME] = DEFAULT_TAG

            i_POLYTAG = tagger.util.string_to_i_POLYTAG(args[MODE])

            if args[OPERATION] == AUTO_OPERATION:
                if args[CONNECTED]:
                    tagger.selection.tag_polys( args[NAME], True, i_POLYTAG )
                else:
                    tagger.selection.tag_polys( args[NAME], False, i_POLYTAG )

                if (
                    not tagger.shadertree.get_masks(pTags = {args[NAME]:i_POLYTAG})
                    and not args[NAME] == DEFAULT_TAG
                    ):

                    mask = tagger.shadertree.build_material(
                        i_POLYTAG = i_POLYTAG,
                        pTag = args[NAME],
                        preset = args[PRESET]
                    )

                    # tagger.shadertree.cleanup()
                    tagger.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == ADD:
                if args[CONNECTED]:
                    tagger.selection.tag_polys( args[NAME], True, i_POLYTAG )
                else:
                    tagger.selection.tag_polys( args[NAME], False, i_POLYTAG )

                mask = tagger.shadertree.build_material(
                    i_POLYTAG = i_POLYTAG,
                    pTag = args[NAME],
                    preset = args[PRESET]
                )

                # tagger.shadertree.cleanup()
                tagger.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == REMOVE:
                if args[CONNECTED]:
                    tagger.selection.tag_polys( DEFAULT_TAG, True, i_POLYTAG )
                else:
                    tagger.selection.tag_polys( DEFAULT_TAG, False, i_POLYTAG )

                # tagger.shadertree.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
