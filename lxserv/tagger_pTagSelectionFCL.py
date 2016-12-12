# python

import lx, lxifc, lxu.command, modo, tagger

CMD_NAME = tagger.CMD_PTAG_SELECTION_FCL

def list_commands():
    fcl = []

    tags = {
        tagger.MATERIAL:set(),
        tagger.PART:set(),
        tagger.PICK:set()
    }

    polys_are_selected = False

    for layer in tagger.items.get_active_layers():
        polys = layer.geometry.polygons.selected

        if polys:
            polys_are_selected = True

        for p in polys:
            if p.tags()[tagger.MATERIAL]:
                tags[tagger.MATERIAL].add(p.tags()[tagger.MATERIAL])
            if p.tags()[tagger.PART]:
                tags[tagger.PART].add(p.tags()[tagger.PART])
            if p.tags()[tagger.PICK]:
                tags[tagger.PICK] = tags[tagger.PICK].union(set(p.tags()[tagger.PICK].split(";")))

    if polys_are_selected:
        for tagType in tags:
            if tags[tagType]:
                fcl.append('- ')
                for tag in tags[tagType]:
                    args = tagger.util.build_arg_string({
                        tagger.TAGTYPE: tagType,
                        tagger.TAG: tag
                    })
                    fcl.append(tagger.CMD_SELECT_ALL_BY_TAG + args)

    return fcl


class tagger_fcl(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class cmd_tagger_fcl(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(tagger.QUERY, lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.not_svc = lx.service.NotifySys()
        self.notifier = None
        self.notifier2 = None

    def cmd_NotifyAddClient (self, argument, object):
        if self.notifier is None:
            self.notifier = self.not_svc.Spawn ("select.event", "polygon +ldt")

        self.notifier.AddClient (object)

        if self.notifier2 is None:
            self.notifier2 = self.not_svc.Spawn ("select.event", "item +ldt")

        self.notifier2.AddClient (object)

    def cmd_NotifyRemoveClient (self, object):
        if self.notifier is not None:
            self.notifier.RemoveClient (object)

        if self.notifier2 is not None:
            self.notifier2.RemoveClient (object)

    def arg_UIValueHints(self, index):
        if index == 0:
            return tagger_fcl(list_commands())

lx.bless(cmd_tagger_fcl, CMD_NAME)
