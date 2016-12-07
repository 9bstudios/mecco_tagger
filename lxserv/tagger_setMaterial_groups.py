#python

import lx, lxu, modo, tagger, traceback

NAME = tagger.NAME
OPERATION = tagger.OPERATION
PRESET = tagger.PRESET

AUTO_OPERATION = tagger.OPERATIONS_AUTO
ADD = tagger.OPERATIONS_ADD
REMOVE = tagger.OPERATIONS_REMOVE

NAME_CMD = tagger.CMD_SET_GROUP

class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(1,3):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[NAME] = self.dyna_String(0) if self.dyna_IsSet(0) else None
            args[OPERATION] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_OPERATION
            args[PRESET] = self.dyna_String(2) if self.dyna_IsSet(2) else None

            selmode = tagger.selection.get_mode()

            if args[OPERATION] in (AUTO_OPERATION,ADD):
                group = tagger.items.group_selected_and_maskable(args[NAME])
                mask = tagger.shadertree.build_material( group, preset = args[PRESET] )
                # tagger.shadertree.cleanup()
                tagger.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == REMOVE:
                items = tagger.items.get_selected_and_maskable()
                groups = tagger.items.get_groups(selected)
                tagger.shadertree.seek_and_destroy(groups)
                # tagger.shadertree.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
