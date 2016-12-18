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
                    'popup': tagger.POPUPS_TAGTYPES_WITH_ALL,
                    'flags': [],
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED_ITEMS,
                    'popup': tagger.POPUPS_REMOVE_ALL_SCOPE,
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
        scope = self.commander_arg_value(1)

        scope_label = tagger.LABEL_SCOPE_SELECTED_ITEMS if scope == tagger.SCOPE_SELECTED_ITEMS else tagger.LABEL_SCOPE_SCENE

        safety = modo.dialogs.yesNo(
            tagger.DIALOGS_REMOVE_ALL_TAGS[0],
            tagger.DIALOGS_REMOVE_ALL_TAGS[1] % (tagType.title(), scope_label.lower())
            )

        if safety == 'yes':
            poly_count = 0
            tag_count = 0

            if scope == tagger.SCOPE_SELECTED_ITEMS:
                meshes = modo.Scene().selectedByType('mesh')
            elif scope == tagger.SCOPE_SCENE:
                meshes = modo.Scene().meshes

            item_count = len(meshes)

            for mesh in meshes:

                # For some reason the tagging operation files if we do
                # more than one in a single `with` statement.
                # Hence we do it three times, once for each tag type.

                if tagType in (tagger.MATERIAL, tagger.ALL):
                    with mesh.geometry as geo:
                        polys = geo.polygons
                        poly_count += len(polys)

                        i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL
                        tag_count += len(tagger.scene.all_tags_by_type(i_POLYTAG))
                        tagger.manage.tag_polys(polys, None, i_POLYTAG)

                if tagType in (tagger.PART, tagger.ALL):
                    with mesh.geometry as geo:
                        polys = geo.polygons
                        poly_count += len(polys)

                        i_POLYTAG = lx.symbol.i_POLYTAG_PART
                        tag_count += len(tagger.scene.all_tags_by_type(i_POLYTAG))
                        tagger.manage.tag_polys(polys, None, i_POLYTAG)

                if tagType in (tagger.PICK, tagger.ALL):
                    with mesh.geometry as geo:
                        polys = geo.polygons
                        poly_count += len(polys)

                        i_POLYTAG = lx.symbol.i_POLYTAG_PICK
                        tag_count += len(tagger.scene.all_tags_by_type(i_POLYTAG))
                        tagger.manage.tag_polys(polys, None, i_POLYTAG)

            modo.dialogs.alert(
                tagger.DIALOGS_REMOVED_ALL_TAGS[0],
                tagger.DIALOGS_REMOVED_ALL_TAGS[1] % (tag_count, poly_count, item_count)
            )

            notifier = tagger.Notifier()
            notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


lx.bless(CommandClass, CMD_NAME)
