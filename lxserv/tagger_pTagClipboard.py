#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = 'tagger.pTagClipboard'

COPY = tagger.symbols.ARGS_COPY
PASTE = tagger.symbols.ARGS_PASTE

MATERIAL = tagger.symbols.FILTER_TYPES_MATERIAL

NAME = tagger.symbols.ARGS_NAME
MODE = tagger.symbols.ARGS_MODE
CONNECTED = tagger.symbols.ARGS_CONNECTED
PRESET = tagger.symbols.ARGS_PRESET

class CMD_tagger(lxu.command.BasicCommand):

    _clipboard = ''

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(CONNECTED, lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(3):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    @classmethod
    def set_clipboard(cls, value):
        cls._clipboard = value

    def basic_Execute(self, msg, flags):
        try:
            mode = self.dyna_String(0) if self.dyna_IsSet(0) else COPY

            if mode == COPY:
                self.set_clipboard(tagger.selection.get_polys()[0].tags()['material'])

            elif mode == PASTE:
                args = {}
                args[NAME] = self._clipboard
                args[MODE] = MATERIAL
                args[CONNECTED] = self.dyna_Bool(1) if self.dyna_IsSet(1) else None

                lx.eval(tagger.symbols.COMMAND_NAME_PTAG + tagger.util.build_arg_string(args))

        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
