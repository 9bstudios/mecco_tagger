#python

import lx, lxu, modo, tagger, traceback

NAME = tagger.ARGS_NAME
MODE = tagger.ARGS_MODE
OPERATION = tagger.ARGS_OPERATION
CONNECTED = tagger.ARGS_CONNECTED
PRESET = tagger.ARGS_PRESET

AUTO_FILTER = tagger.FILTER_TYPES_AUTO
MATERIAL = tagger.FILTER_TYPES_MATERIAL
PART = tagger.FILTER_TYPES_PART
PICK = tagger.FILTER_TYPES_PICK
ITEM = tagger.FILTER_TYPES_ITEM
ACTIVE = tagger.FILTER_TYPES_ACTIVE
GLOC = tagger.FILTER_TYPES_GLOC
GROUP = tagger.FILTER_TYPES_GROUP

AUTO_OPERATION = tagger.OPERATIONS_AUTO
OVERRIDE = tagger.OPERATIONS_OVERRIDE
ADD = tagger.OPERATIONS_ADD
REMOVE = tagger.OPERATIONS_REMOVE

NAME_CMD = tagger.COMMAND_NAME_BASE


class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME, lx.symbol.sTYPE_STRING)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(CONNECTED, lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(5):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[NAME] = self.dyna_String(0) if self.dyna_IsSet(0) else None
            args[MODE] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_FILTER
            args[OPERATION] = self.dyna_String(2) if self.dyna_IsSet(2) else None
            args[CONNECTED] = self.dyna_Bool(3) if self.dyna_IsSet(3) else None
            args[PRESET] = self.dyna_String(4) if self.dyna_IsSet(4) else None

            selmode = tagger.selection.get_mode()

            if args[MODE] == AUTO_FILTER:
                if selmode in ['polygon','ptag']:
                    args[MODE] = MATERIAL
                    if args[OPERATION] == REMOVE:
                        args[NAME] = REMOVE

                elif selmode in ['edge','vertex']:
                    args[MODE] = MATERIAL
                    args[CONNECTED] = True
                elif selmode == ITEM:
                    if len(tagger.items.get_selected_and_maskable()) == 0:
                        args[MODE] = ACTIVE
                    elif len(tagger.items.get_selected_and_maskable()) == 1:
                        args[MODE] = ITEM
                    else:
                        args[MODE] = GROUP
                else:
                    return False


            if args[MODE] in (MATERIAL,PART,PICK):
                if args[OPERATION] == REMOVE:
                    args[NAME] = REMOVE
                lx.eval(tagger.COMMAND_NAME_PTAG + tagger.util.build_arg_string(args))

            elif args[MODE] in (ITEM,ACTIVE):
                del args[NAME]
                del args[CONNECTED]
                lx.eval(tagger.COMMAND_NAME_ITEM + tagger.util.build_arg_string(args))

            elif args[MODE] == GROUP:
                del args[MODE]
                del args[CONNECTED]
                lx.eval(tagger.COMMAND_NAME_GROUP + tagger.util.build_arg_string(args))


        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
