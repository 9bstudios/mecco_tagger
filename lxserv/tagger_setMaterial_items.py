#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_ITEM

class CMD_tagger(lxu.command.BasicCommand):
    _last_used = [
        tagger.POPUPS_ADD_REMOVE[0][0],
        tagger.RANDOM,
    ]
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add(tagger.OPERATION, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.PRESET, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_OPERATION)

        if index == 1:
            hints.Label(tagger.LABEL_PRESET)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger.PopupClass(tagger.POPUPS_ADD_REMOVE)

        if index == 1:
            popup_list = [(tagger.RANDOM, tagger.LABEL_RANDOM_COLOR)]
            popup_list.extend(tagger.presets.list_presets())
            return tagger.PopupClass(popup_list)

    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])
        self.attr_SetString(1, self._last_used[1])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        try:
            operation = self.dyna_String(0) if self.dyna_IsSet(0) else self._last_used[0]
            self.set_last_used(0, self.dyna_String(0))

            preset = self.dyna_String(1) if self.dyna_IsSet(1) else self._last_used[1]
            self.set_last_used(1, self.dyna_String(1))

            if preset == tagger.RANDOM:
                preset = None

            items = tagger.items.get_selected_and_maskable()

            if operation == tagger.ADD:
                for item in items:
                    mask = tagger.shadertree.build_material( item, preset = preset )
                    tagger.shadertree.move_to_base_shader(mask)

            if operation == tagger.REMOVE:
                tagger.shadertree.seek_and_destroy(items)


        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
