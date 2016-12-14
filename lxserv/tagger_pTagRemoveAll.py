# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_REMOVEALL
DEFAULTS = [tagger.PART, '', False]

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.PART,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': [],
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)

        safety = modo.dialogs.yesNo(tagger.DIALOGS_REMOVE_ALL_TAGS[0], tagger.DIALOGS_REMOVE_ALL_TAGS[1] % tagType)

        if safety == 'yes':
            for mesh in modo.Scene().meshes:
                with mesh.geometry as geo:
                    polys = geo.polygons
                    tagger.manage.tag_polys(polys, None, tagger.util.string_to_i_POLYTAG(tagType))

lx.bless(CommandClass, CMD_NAME)
