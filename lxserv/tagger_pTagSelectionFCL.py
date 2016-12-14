# python

import lx, lxifc, lxu.command, modo, tagger

CMD_NAME = tagger.CMD_PTAG_SELECTION_FCL

class MeshEditorClass(tagger.MeshEditorClass):
    def commander_mesh_edit_action(self):
        tags = [
            set(),
            set(),
            set()
        ]

        stringTag = lx.object.StringTag()
        stringTag.set(polygon_accessor)

        for island in list_of_poly_islands:
            for poly in island:
                polygon_accessor.Select(poly)

                material = stringTag.Get(lx.symbol.i_POLYTAG_MATERIAL)
                if material:
                    tags[0].add(material)

                part = stringTag.Get(lx.symbol.i_POLYTAG_PART)
                if part:
                    tags[1].add(part)

                pick = stringTag.Get(lx.symbol.i_POLYTAG_PICK)
                if pick:
                    tags[2].update(pick.split(";"))

        return tags

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.QUERY,
                    'label': tagger.LABEL_QUERY,
                    'datatype': 'integer',
                    'value': '',
                    'fcl': self.list_commands(),
                    'flags': ['query'],
                }
            ]

    def commander_notifiers(self):
        return [("select.event", "polygon +ldt"),("select.event", "item +ldt")]

    def list_commands(self):
        fcl = []

        mesh_editor = MeshEditorClass(None,[])
        tags = mesh_editor.do_mesh_edit()

        for n in range(len(tags)):
            if not tags[n]:
                continue

            for tag in sorted(tags[n]):
                tagType = [tagger.MATERIAL, tagger.PART, tagger.PICK][n]
                fcl.append("%s %s {%s}" % (tagger.CMD_SELECT_ALL_BY_TAG, tagType, tag))

        return fcl


lx.bless(CommandClass, CMD_NAME)
