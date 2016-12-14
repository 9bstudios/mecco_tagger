# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_SET
DEFAULTS = [tagger.MATERIAL, '', False]

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
                    'flags': []
                }, {
                    'name': tagger.TAG,
                    'label': tagger.LABEL_TAG,
                    'datatype': 'string',
                    'value': "",
                    'flags': ['optional'],
                    'sPresetText': tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL)
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        tag = self.commander_arg_value(1)
        connected = self.commander_arg_value(2)

        tagger.selection.tag_polys(tag, connected, tagger.util.string_to_i_POLYTAG(tagType))

    def basic_ButtonName(self):
        tagType = self.commander_arg_value(0)
        tag = self.commander_arg_value(1)

        return "%s %s: %s" % (tagger.LABEL_SET, tagType, tag)

lx.bless(CommandClass, CMD_NAME)
