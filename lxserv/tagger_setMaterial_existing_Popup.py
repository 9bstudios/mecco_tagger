
import lx, lxifc, lxu.command, tagger

CMD_NAME = tagger.CMD_SET_EXISTING_POPUP

def tagsHack(tags):
    hackedTags = []

    if not tags:
        hackedTags.append((None, tagger.LABEL_NONE))

    for tag in sorted(tags):
        tag_internal = "__".join((tag[0], tag[1]))
        tag_user = "%s (%s)" % (tag[1], tag[0])
        hackedTags.append((tag_internal, tag_user))

    return hackedTags

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAG,
                    'label': tagger.LABEL_TAG_WITH_MASKED,
                    'datatype': 'string',
                    'value': '',
                    'popup': tagsHack(tagger.items.get_all_masked_tags()),
                    'flags': ['query'],
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'flags': ['optional'],
                    'sPresetText': tagger.POPUPS_SCOPE
                }
            ]

    def commander_execute(self, msg, flags):
        if not self.commander_arg_value(0):
            return

        tag = self.commander_arg_value( 0).split("__")
        connected = self.commander_arg_value(1)

        args = tagger.util.build_arg_string({
            tagger.TAGTYPE: tag[0],
            tagger.TAG: tag[1],
            tagger.SCOPE: connected
        })

        lx.eval(tagger.CMD_PTAG_SET + args)

    def commander_notifiers(self):
        return [('notifier.editAction',''),("select.event", "item +ldt")]


lx.bless(CommandClass, CMD_NAME)