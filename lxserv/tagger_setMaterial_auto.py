#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_MATERIAL


class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            selmode = tagger.selection.get_mode()

            if selmode == 'item':
                lx.eval(tagger.CMD_SET_ITEM)

            elif selmode in ['vertex', 'edge', 'polygon']:
                lx.eval(tagger.CMD_SET_PTAG)

        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
