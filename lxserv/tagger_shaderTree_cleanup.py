#python

import lx, lxu, modo, traceback, tagger

NAME_CMD = tagger.CMD_SHADERTREE_CLEANUP


class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.DEL_EMPTY,
                    'label': tagger.LABEL_DELETE_EMPTY_GROUPS,
                    'datatype': 'boolean',
                    'value': True,
                    'flags': []
                }, {
                    'name': tagger.DEL_UNUSED,
                    'label': tagger.LABEL_DELETE_UNUSED_GROUPS,
                    'datatype': 'boolean',
                    'value': True,
                    'flags': []
                }
            ]

    def commander_execute(self, msg, flags):
        del_empty = self.commander_arg_value(0)
        del_unused = self.commander_arg_value(1)

        hitlist = set()
        for m in modo.Scene().iterItems(lx.symbol.sITYPE_MASK):
            if not m.children() and del_empty:
                hitlist.add(m)

            if del_unused:
                i_POLYTAG = tagger.util.string_to_i_POLYTAG(m.channel(lx.symbol.sICHAN_MASK_PTYP).get())

                sICHAN_MASK_PTAG = m.channel(lx.symbol.sICHAN_MASK_PTAG).get()

                if (sICHAN_MASK_PTAG and not tagger.items.get_layers_by_pTag(sICHAN_MASK_PTAG,i_POLYTAG)):
                    hitlist.add(m)

        tagger.util.safe_removeItems(hitlist, True)


lx.bless(CommandClass, NAME_CMD)
