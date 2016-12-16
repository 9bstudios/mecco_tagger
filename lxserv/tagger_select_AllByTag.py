# python

import lx, lxu, lxifc, modo, tagger, traceback

CMD_NAME = tagger.CMD_SELECT_ALL_BY_TAG

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
                    'flags': [],
                }, {
                    'name': tagger.TAG,
                    'label': tagger.LABEL_TAG,
                    'datatype': 'string',
                    'value': '',
                    'popup': tagger.scene.all_tags(),
                    'flags': ['optional'],
                }
            ]

    def basic_Icon(self):
        if self.commander_arg_value(0):
            if self.commander_arg_value(0) == tagger.MATERIAL:
                return 'tagger.selectAllByMaterial'
            if self.commander_arg_value(0) == tagger.PART:
                return 'tagger.selectAllByPart'
            if self.commander_arg_value(0) == tagger.PICK:
                return 'tagger.selectAllBySet'

        return 'tagger.selectAllByTag'

    def basic_ButtonName(self):
        label = []
        label.append(tagger.LABEL_SELECT_ALL)
        if self.commander_arg_value(0):
            label.append(tagger.util.i_POLYTAG_to_label(self.commander_arg_value(0)))
        label.append(tagger.LABEL_TAG)
        if self.commander_arg_value(1):
            label.append(": %s" % self.commander_arg_value(1))
        return " ".join(label)

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        tag = self.commander_arg_value(1)

        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

        tags = []

        if tag:
            tags = tag.split(";")

        elif not tag:
            tagStrings = tagger.selection.get_ptags(i_POLYTAG)
            for tagString in tagStrings:
                tags.extend(tagString.split(";"))

        for tag in tags:
            if tagType in ['material', 'part']:
                lx.eval("select.polygon add %s face {%s}" % (tagType, tag))
            elif tagType == 'pick':
                lx.eval("select.useSet {%s} select" % tag)


lx.bless(CommandClass, CMD_NAME)