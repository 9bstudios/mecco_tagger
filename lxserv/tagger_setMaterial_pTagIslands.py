# python

import lx, tagger, modo

CMD_NAME = tagger.CMD_SET_PTAG_ISLANDS


class CommandClass(tagger.Commander):
    _commander_default_values = []

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
        args = {
            'tag': self.commander_arg_value(0),
            'tagType': self.commander_arg_value(1)
        }

        mesh_editor = MeshEditorClass(args, [lx.symbol.f_MESHEDIT_POL_TAGS])
        mesh_editor.do_mesh_edit()

        modo.dialogs.alert(
            tagger.DIALOGS_TAGGED_POLYS_COUNT[0],
            tagger.DIALOGS_TAGGED_POLYS_COUNT[1] % (mesh_editor.poly_counter, mesh_editor.island_counter)
            )

lx.bless(CommandClass, CMD_NAME)


class MeshEditorClass(tagger.MeshEditorClass):
    poly_counter = 0
    island_counter = 0

    def mesh_edit_action(self):
        i_POLYTAG = tagger.util.string_to_i_POLYTAG(self.args['tagType'])
        stringTag = lx.object.StringTag()
        stringTag.set(self.polygon_accessor)

        islands = self.get_polys_by_island()

        for i, island in enumerate(islands):

            self.island_counter += 1
            pTag = "_".join((self.args['tag'], str(i)))
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag)

            for poly in island:
                self.polygon_accessor.Select(poly)
                stringTag.Set(i_POLYTAG, pTag)
                self.poly_counter += 1
