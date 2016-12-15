#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_REMOVE_MATERIAL

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):

        selmode = tagger.selection.get_mode()

        if selmode == 'item':
            lx.eval("%s %s" % (tagger.CMD_SET_ITEM, tagger.REMOVE))

        elif selmode in ['vertex', 'edge', 'polygon']:
            lx.eval("%s %s %s %s" % (tagger.CMD_REMOVE_PTAG, tagger.MATERIAL, tagger.SCOPE_FLOOD, 'true'))

lx.bless(CommandClass, NAME_CMD)
