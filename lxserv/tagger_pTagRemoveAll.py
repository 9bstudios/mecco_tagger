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

    def basic_Icon(self):
        if self.commander_arg_value(0):
            if self.commander_arg_value(0) == tagger.MATERIAL:
                return 'tagger.removeAllByMaterial'
            elif self.commander_arg_value(0) == tagger.PART:
                return 'tagger.removeAllByPart'
            elif self.commander_arg_value(0) == tagger.PICK:
                return 'tagger.removeAllBySet'

        return 'tagger.pTagRemoveAll'

    def basic_ButtonName(self):
        if self.commander_arg_value(0):
            label = []
            label.append(tagger.LABEL_REMOVE_ALL)
            label.append(tagger.util.i_POLYTAG_to_label(self.commander_arg_value(0)))
            label.append(tagger.LABEL_TAGS)
            return " ".join(label)

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

        safety = modo.dialogs.yesNo(tagger.DIALOGS_REMOVE_ALL_TAGS[0], tagger.DIALOGS_REMOVE_ALL_TAGS[1] % tagType)
        poly_count = 0
        tag_count = len(tagger.scene.all_tags_by_type(i_POLYTAG))
        item_count = len(modo.Scene().selectedByType('mesh'))

        if safety == 'yes':
            for mesh in modo.Scene().selectedByType('mesh'):
                with mesh.geometry as geo:
                    polys = geo.polygons
                    poly_count += len(polys)
                    tagger.manage.tag_polys(polys, None, i_POLYTAG)

        modo.dialogs.alert(
            tagger.DIALOGS_REMOVED_ALL_TAGS[0],
            tagger.DIALOGS_REMOVED_ALL_TAGS[1] % (tag_count, tagType, poly_count, item_count)
        )

lx.bless(CommandClass, CMD_NAME)
