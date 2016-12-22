# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_SET
DEFAULTS = [tagger.MATERIAL, '', False]

def tags_list():
    return tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL)

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': []
                }, {
                    'name': tagger.TAG,
                    'label': tagger.LABEL_TAG,
                    'datatype': 'string',
                    'value': "",
                    'flags': [],
                    'sPresetText': tags_list
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }
            ]

    def basic_Icon(self):
        if self.commander_arg_value(0):
            if self.commander_arg_value(0) == tagger.MATERIAL:
                return 'tagger.pTagSetMaterial'
            if self.commander_arg_value(0) == tagger.PART:
                return 'tagger.pTagSetPart'
            if self.commander_arg_value(0) == tagger.PICK:
                return 'tagger.pTagSetSet'

        return 'tagger.pTagSet'

    def basic_ButtonName(self):
        label = []
        label.append(tagger.LABEL_SET)

        if self.commander_arg_value(0):
            label.append(tagger.util.i_POLYTAG_to_label(self.commander_arg_value(0)))

        label.append(tagger.LABEL_TAG)

        if self.commander_arg_value(1):
            label.append(": %s" % self.commander_arg_value(1))

        if self.commander_arg_value(2):
            if self.commander_arg_value(2) != tagger.SCOPE_SELECTED:
                label.append("(%s)" % self.commander_arg_value(2))

        return " ".join(label)

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        tag = self.commander_arg_value(1)
        connected = self.commander_arg_value(2)

        tagger.selection.tag_polys(tag, connected, tagger.util.string_to_i_POLYTAG(tagType))

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


lx.bless(CommandClass, CMD_NAME)
