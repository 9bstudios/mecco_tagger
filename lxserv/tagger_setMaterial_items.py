#python

import lx, lxu, modo, tagger, traceback

MODE = tagger.symbols.ARGS_MODE
OPERATION = tagger.symbols.ARGS_OPERATION
PRESET = tagger.symbols.ARGS_PRESET

AUTO_FILTER = tagger.symbols.FILTER_TYPES_AUTO
ITEM = tagger.symbols.FILTER_TYPES_ITEM
ACTIVE = tagger.symbols.FILTER_TYPES_ACTIVE
GLOC = tagger.symbols.FILTER_TYPES_GLOC
GROUP = tagger.symbols.FILTER_TYPES_GROUP

AUTO_OPERATION = tagger.symbols.OPERATIONS_AUTO
ADD = tagger.symbols.OPERATIONS_ADD
REMOVE = tagger.symbols.OPERATIONS_REMOVE

NAME_CMD = tagger.symbols.COMMAND_NAME_ITEM

class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(3):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[MODE] = self.dyna_String(0) if self.dyna_IsSet(0) else AUTO_FILTER
            args[OPERATION] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_OPERATION
            args[PRESET] = self.dyna_String(2) if self.dyna_IsSet(2) else None

            selmode = tagger.selection.get_mode()

            items = (
                tagger.items.get_active_layers() if args[MODE] == ACTIVE
                else tagger.items.get_selected_and_maskable()
            )

            if args[OPERATION] == AUTO_OPERATION:
                for item in items:
                    if tagger.shadertree.get_masks(item):
                        tagger.shadertree.seek_and_destroy(item)
                    mask = tagger.shadertree.build_material( item, preset = args[PRESET] )
                    # tagger.shadertree.cleanup()
                    tagger.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == ADD:
                for item in items:
                    mask = tagger.shadertree.build_material( item, preset = args[PRESET] )
                    # tagger.shadertree.cleanup()
                    tagger.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == REMOVE:
                items = modo.Scene().selected
                tagger.shadertree.seek_and_destroy(items)
                # tagger.shadertree.cleanup()


        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
