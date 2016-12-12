# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_CONVERT_PTAGS

class CommandClass(tagger.Commander):
    _commander_last_used = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.FROM_TAG_TYPE,
                    'label': tagger.LABEL_FROM_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': [],
                }, {
                    'name': tagger.TO_TAG_TYPE,
                    'label': tagger.LABEL_TO_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.PICK,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': []
                }
            ]

    def commander_execute(self, msg, flags):
        fromTagType = self.commander_arg_value(0)
        toTagType = self.commander_arg_value(1)

        tagger.selection.convert_tags(
            tagger.util.string_to_i_POLYTAG(fromTagType),
            tagger.util.string_to_i_POLYTAG(toTagType)
            )

lx.bless(CommandClass, CMD_NAME)
