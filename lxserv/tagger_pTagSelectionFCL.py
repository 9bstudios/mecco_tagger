# python

import lx, lxifc, lxu.command, modo, tagger

CMD_NAME = tagger.CMD_PTAG_SELECTION_FCL

def list_commands():
    fcl = []

    tags = {
        tagger.MATERIAL:set(),
        tagger.PART:set(),
        tagger.PICK:set()
    }

    polys_are_selected = False

    for layer in tagger.items.get_active_layers():
        polys = layer.geometry.polygons.selected

        if polys:
            polys_are_selected = True

        for p in polys:
            if p.tags()[tagger.MATERIAL]:
                tags[tagger.MATERIAL].add(p.tags()[tagger.MATERIAL])
            if p.tags()[tagger.PART]:
                tags[tagger.PART].add(p.tags()[tagger.PART])
            if p.tags()[tagger.PICK]:
                tags[tagger.PICK] = tags[tagger.PICK].union(set(p.tags()[tagger.PICK].split(";")))

    if polys_are_selected:
        for tagType in tags:
            if tags[tagType]:
                fcl.append('- ')
                for tag in tags[tagType]:
                    args = tagger.util.build_arg_string({
                        tagger.TAGTYPE: tagType,
                        tagger.TAG: tag
                    })
                    fcl.append(tagger.CMD_SELECT_ALL_BY_TAG + args)

    return fcl


class CommandClass(tagger.Commander):
    _commander_last_used = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.QUERY,
                    'label': tagger.LABEL_QUERY,
                    'datatype': 'integer',
                    'value': '',
                    'fcl': list_commands(),
                    'flags': ['query'],
                }
            ]

    def commander_execute(self, msg, flags):
        pass

    def commander_notifiers(self):
        return [("select.event", "polygon +ldt"),("select.event", "item +ldt")]


lx.bless(CommandClass, CMD_NAME)
