# python

import lx, lxifc, lxu, modo
import tagger
from os.path import basename, splitext

CMD_NAME = tagger.CMD_SET_PTAG

class CommandClass(tagger.Commander):
    _commander_last_used = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAG,
                    'datatype': 'string',
                    'value': "",
                    'flags': [],
                    'sPresetText': tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL)
                }, {
                    'name': tagger.PRESET,
                    'datatype': 'string',
                    'value': tagger.RANDOM,
                    'popup': tagger.presets.presets_popup(),
                    'flags': ['optional']
                }, {
                    'name': tagger.SCOPE,
                    'datatype': 'string',
                    'value': tagger.POPUPS_SCOPE[2][0],
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }, {
                    'name': tagger.TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.POPUPS_TAGTYPES[0][0],
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': ['optional']
                }, {
                    'name': tagger.WITH_EXISTING,
                    'datatype': 'string',
                    'value': tagger.POPUPS_WITH_EXISTING[0][0],
                    'popup': tagger.POPUPS_WITH_EXISTING,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        pTag = self.commander_arg_value(0)

        preset = self.commander_arg_value(1)
        preset = None if preset == tagger.RANDOM else preset

        connected = self.commander_arg_value(2)

        tagType = self.commander_arg_value(3)
        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

        withExisting = self.commander_arg_value(4)

        if not pTag and (not preset or not preset.endswith(".lxp")):
            pTag = tagger.DEFAULT_MATERIAL_NAME

        elif not pTag and preset.endswith(".lxp"):
            pTag = splitext(basename(preset))[0]

        # find any existing masks for this pTag
        existing_masks = tagger.shadertree.get_masks( pTags = { pTag: i_POLYTAG })

        # tag the polys
        tagger.selection.tag_polys(pTag, connected, i_POLYTAG)

        # build a new mask if we need one
        if not existing_masks or (existing_masks and withExisting != tagger.POPUPS_WITH_EXISTING[0][0]):
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag, preset = preset)

        if existing_masks and withExisting == tagger.POPUPS_WITH_EXISTING[1][0]:
            tagger.util.safe_removeItems(existing_masks, True)

        elif existing_masks and withExisting == tagger.POPUPS_WITH_EXISTING[2][0]:
            tagger.shadertree.consolidate(pTags = { pTag: i_POLYTAG })

lx.bless(CommandClass, CMD_NAME)
