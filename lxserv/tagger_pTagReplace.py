# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_REPLACE
DEFAULTS = [tagger.MATERIAL, '', '']

def selected_tag(tagType):
    active_layers = tagger.items.get_active_layers()
    polys = []
    if active_layers:
        for layer in active_layers:
            polys.extend(layer.geometry.polygons.selected)
        if polys:
            return polys[0].tags()[tagType]
        elif not polys:
            return DEFAULTS[1]
    elif not active:
        return DEFAULTS[1]

class CommandClass(tagger.Commander):
    _commander_last_used = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': [],
                }, {
                    'name': tagger.REPLACETAG,
                    'label': tagger.LABEL_REPLACE_TAG,
                    'datatype': 'string',
                    'value': selected_tag(tagger.MATERIAL),
                    'flags': [],
                    'sPresetText': tagger.scene.all_tags()
                }, {
                    'name': tagger.WITHTAG,
                    'label': tagger.LABEL_WITH_TAG,
                    'datatype': 'string',
                    'value': "",
                    'flags': [],
                    'sPresetText': tagger.scene.all_tags()
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        replaceTag = self.commander_arg_value(1)
        withTag = self.commander_arg_value(2)

        hitcount = 0

        meshes_with_pTag = tagger.scene.meshes_with_pTag(replaceTag, i_POLYTAG)

        for mesh in meshes_with_pTag:
            with mesh.geometry as geo:
                hitlist = set()
                for poly in geo.polygons:

                    if tagType in [tagger.MATERIAL, tagger.PART]:
                        if poly.getTag(i_POLYTAG) == replaceTag:
                            hitlist.add(poly)
                            hitcount += 1

                    elif tagType == tagger.PICK:
                        if not poly.getTag(i_POLYTAG):
                            continue

                        pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                        if replaceTag in pickTags:
                            hitlist.add(poly)
                            hitcount += 1


            with mesh.geometry as geo:
                for poly in hitlist:

                    if tagType in [tagger.MATERIAL, tagger.PART]:
                        poly.setTag(i_POLYTAG, withTag)

                    elif tagType == tagger.PICK:
                        pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                        pickTags.discard(replaceTag)
                        pickTags.add(withTag)
                        poly.setTag(i_POLYTAG, ";".join(pickTags))


        if hitcount == 0:
            modo.dialogs.alert(tagger.DIALOGS_TAG_NOT_FOUND[0], tagger.DIALOGS_TAG_NOT_FOUND[1] % (tagType, replaceTag))

        elif hitcount >= 1:
            modo.dialogs.alert(tagger.DIALOGS_TAG_REPLACED[0], tagger.DIALOGS_TAG_REPLACED[1] % (hitcount, tagType, replaceTag))


lx.bless(CommandClass, CMD_NAME)
