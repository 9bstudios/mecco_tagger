# python

import lx, lxifc, lxu.command, modo, tagger

CMD_NAME = tagger.CMD_PTAG_SELECTION_FCL

def list_commands():
    fcl = []

    for layer in tagger.items.get_active_layers():
        polys = layer.geometry.polygons.selected

    if not polys:
        return fcl

    tags = [
        set(),
        set(),
        set()
    ]

    for layer in tagger.items.get_active_layers():
        polys = layer.geometry.polygons.selected

        for p in polys:
            pTags = p.tags()

            material = pTags.get(tagger.MATERIAL)
            if material:
                tags[0].add(material)

            part = pTags.get(tagger.PART)
            if part:
                tags[1].add(part)

            pick = pTags.get(tagger.PICK)
            if pick:
                tags[2].update(pick.split(";"))

    for n in range(len(tags)):
        if not tags[n]:
            continue

        fcl.append('- ')
        for tag in sorted(tags[n]):
            tagType = [tagger.MATERIAL, tagger.PART, tagger.PICK][n]
            fcl.append("%s %s {%s}" % (tagger.CMD_SELECT_ALL_BY_TAG, tagType, tag))

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

    def commander_notifiers(self):
        return [("select.event", "polygon +ldt"),("select.event", "item +ldt")]


lx.bless(CommandClass, CMD_NAME)
