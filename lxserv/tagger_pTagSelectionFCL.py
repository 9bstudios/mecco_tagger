# python

import lx, lxifc, lxu.command, modo, tagger, random

CMD_NAME = tagger.CMD_PTAG_SELECTION_FCL

global_tags = None

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

        global global_tags
        global_tags = [
            set(),
            set(),
            set()
        ]

        mesh_editor = MeshEditorClass()
        mesh_editor.do_mesh_read()
        tags = global_tags

        if len(tags) > tagger.MAX_FCL:
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

    def mesh_read_action(self):
        global global_tags

        stringTag = lx.object.StringTag()
        stringTag.set(self.polygon_accessor)

        selected_polys = self.get_polys_by_selected()

        if len(selected_polys) <= tagger.MAX_FCL:

            for poly in selected_polys:
                self.polygon_accessor.Select(poly)

                material = stringTag.Get(lx.symbol.i_POLYTAG_MATERIAL)
                if material:
                    global_tags[0].add(material)

                part = stringTag.Get(lx.symbol.i_POLYTAG_PART)
                if part:
                    global_tags[1].add(part)

                pick = stringTag.Get(lx.symbol.i_POLYTAG_PICK)
                if pick:
                    global_tags[2].update(pick.split(";"))
