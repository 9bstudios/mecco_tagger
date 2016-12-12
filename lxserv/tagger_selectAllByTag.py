# python

import lx, lxu, lxifc, modo, tagger, traceback

NAME_CMD = tagger.CMD_SELECT_ALL_BY_TAG

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
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)

        tags = set()
        for p in tagger.selection.get_polys():
            tag = p.tags()[tagType]
            if tag:
                tag = tag.split(";")
            if not tag:
                tag = []
            tags.update(tag)

        for tag in tags:
            lx.eval("select.polygon add %s face %s" % (tagType, tag))

lx.bless(CommandClass, CMD_NAME)
