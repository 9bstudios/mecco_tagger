#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_GROUP

class CMD_tagger(lxu.command.BasicCommand):
    _last_used = [
        tagger.DEFAULT_GROUP_NAME,
        tagger.ADD,
        tagger.RANDOM
    ]

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(tagger.NAME, lx.symbol.sTYPE_STRING)

        self.dyna_Add(tagger.OPERATION, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add(tagger.PRESET, lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label(tagger.LABEL_GROUP_NAME)

        if index == 1:
            hints.Label(tagger.LABEL_OPERATION)

        if index == 2:
            hints.Label(tagger.LABEL_PRESET)

    def arg_UIValueHints(self, index):
        if index == 1:
            return tagger.PopupClass(tagger.POPUPS_ADD_REMOVE)

        if index == 2:
            popup_list = [(tagger.RANDOM, tagger.LABEL_RANDOM_COLOR)]
            popup_list.extend(tagger.presets.list_presets())
            return tagger.PopupClass(popup_list)


    def cmd_DialogInit(self):
        self.attr_SetString(0, self._last_used[0])
        self.attr_SetString(1, self._last_used[1])
        self.attr_SetString(2, self._last_used[2])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    def basic_Execute(self, msg, flags):
        try:
            group_name = self.dyna_String(0) if self.dyna_IsSet(0) else self._last_used[0]
            self.set_last_used(0, group_name)

            operation = self.dyna_String(1) if self.dyna_IsSet(1) else self._last_used[1]
            self.set_last_used(1, operation)

            preset = self.dyna_String(2) if self.dyna_IsSet(2) else self._last_used[2]
            self.set_last_used(2, preset)

            preset = None if preset == tagger.RANDOM else preset

            selmode = tagger.selection.get_mode()

            if operation == tagger.ADD:
                group = tagger.items.group_selected_and_maskable(group_name)
                mask = tagger.shadertree.build_material( group, preset = preset )
                tagger.shadertree.move_to_base_shader(mask)

            if operation == tagger.REMOVE:
                items = tagger.items.get_selected_and_maskable()
                groups = tagger.items.get_groups(selected)
                tagger.shadertree.seek_and_destroy(groups)

        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
