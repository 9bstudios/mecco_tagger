# python

import lx, lxu, lxifc, modo, tagger, traceback

CMD_NAME = tagger.CMD_SELECT_ALL_BY_TAG

class CommandClass(tagger.Commander):
    _commander_last_used = []

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

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        tag = self.commander_arg_value(1)

        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

        if tag:
            tags = tag.split(";")

        elif not tag:
            tags = tagger.selection.get_ptags(i_POLYTAG)

        for tag in tags:
            lx.eval("select.polygon add %s face {%s}" % (tagType, tag))

    def basic_ButtonName(self):
        tagType = self.commander_arg_value(0)
        tag = self.commander_arg_value(1)
        if tag:
            return "%s (%s)" % (tag, tagger.util.i_POLYTAG_to_label(tagType))

lx.bless(CommandClass, CMD_NAME)
