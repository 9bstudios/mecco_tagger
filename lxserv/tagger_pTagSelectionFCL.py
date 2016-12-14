# python

import lx, lxifc, lxu.command, modo, tagger, random

CMD_NAME = tagger.CMD_PTAG_SELECTION_FCL


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

        mesh_editor = MeshEditorClass()
        mesh_editor.do_mesh_read()
        tags = mesh_editor.tags

        if not tags:
            return fcl

        for n in range(len(tags)):
            if not tags[n]:
                continue

            for tag in sorted(tags[n]):
                tagType = [tagger.MATERIAL, tagger.PART, tagger.PICK][n]
                fcl.append("%s %s {%s}" % (tagger.CMD_SELECT_ALL_BY_TAG, tagType, tag))

        return fcl

lx.bless(CommandClass, CMD_NAME)


class MeshEditorClass(tagger.MeshEditorClass):
    tags = [
        set(),
        set(),
        set()
    ]

    def mesh_read_action(self):
        stringTag = lx.object.StringTag()
        stringTag.set(self.polygon_accessor)

        selected_polys = self.get_polys_by_selected()

        for poly in selected_polys:
            self.polygon_accessor.Select(poly)

            material = stringTag.Get(lx.symbol.i_POLYTAG_MATERIAL)
            if material:
                self.tags[0].add(material)

            part = stringTag.Get(lx.symbol.i_POLYTAG_PART)
            if part:
                self.tags[1].add(part)

            pick = stringTag.Get(lx.symbol.i_POLYTAG_PICK)
            if pick:
                self.tags[2].update(pick.split(";"))
