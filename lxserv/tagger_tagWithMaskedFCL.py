# python

import lx, lxifc, lxu.command, modo, tagger

CMD_NAME = tagger.CMD_TAG_WITH_MASKED_FCL

def list_commands():
    fcl = []

    if tagger.selection.get_mode() != 'polygon':
        return fcl

    material_tags = tagger.items.get_all_masked_tags()

    if material_tags:
        fcl.append('- ')

    for tag in sorted(material_tags):
        fcl.append('%s %s {%s}' % (tagger.CMD_PTAG_SET, tag[0], tag[1]))

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
