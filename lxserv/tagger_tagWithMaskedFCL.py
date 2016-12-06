# python

import lx, lxifc, lxu.command, modo, tagger

CMD_NAME = 'tagger.tagWithMaskedFCL'

def list_commands():
    fcl = []

    material_tags = tagger.items.get_all_material_tags()

    for tag in material_tags:
        fcl.append('tagger.pTagSet material %s' % tag)

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
        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.not_svc = lx.service.NotifySys()
        self.notifier = None

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

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(cmd_tagger_fcl, CMD_NAME)
