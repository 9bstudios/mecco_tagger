# python

import lx, tagger

CMD_NAME = tagger.CMD_SET_PTAG_ISLANDS

class CommandClass(tagger.Commander):
    _commander_last_used = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAG,
                    'label': tagger.LABEL_TAG,
                    'datatype': 'string',
                    'value': '',
                    'sPresetText': sorted(tagger.scene.all_tags()),
                    'flags': ['optional'],
                }, {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'flags': [],
                    'popup': tagger.POPUPS_TAGTYPES
                }
            ]

    def commander_execute(self, msg, flags):
        self.commander_mesh_edit()

    def commander_mesh_edit_action(self, polygon_accessor, point_accessor, list_of_poly_islands):
        tag = self.commander_arg_value(0)
        tagType = self.commander_arg_value(1)
        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

        stringTag = lx.object.StringTag()
        stringTag.set(polygon_accessor)

        for i, island in enumerate(list_of_poly_islands):

            pTag = "_".join((tag, str(i)))
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag)

            for poly in island:
                polygon_accessor.Select(poly)
                stringTag.Set(i_POLYTAG, pTag)


lx.bless(CommandClass, CMD_NAME)
