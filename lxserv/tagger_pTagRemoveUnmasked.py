# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_REMOVE_UNMASKED

MATERIAL = 'material'
PICK = 'pick'
PART = 'part'

class MeshEditorClass(tagger.MeshEditorClass):

    hitcount = 0

    def mesh_edit_action(self):

        tagType = self.args[0]
        replaceTag = self.args[1]
        i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)

        hitlist = set()

        stringTag = lx.object.StringTag()
        stringTag.set(self.polygon_accessor)

        nPolys = self.mesh.PolygonCount()

        for eachPoly in xrange(nPolys):
            self.polygon_accessor.SelectByIndex(eachPoly)
            if tagType in [MATERIAL, PART]:
                if stringTag.Get(i_POLYTAG) == replaceTag:
                   hitlist.add(eachPoly)
                   self.hitcount += 1

            elif tagType == PICK:
                if not stringTag.Get(i_POLYTAG):
                    continue

                pickTags = set(stringTag.Get(i_POLYTAG).split(";"))
                if replaceTag in pickTags:
                    hitlist.add(eachPoly)
                    self.hitcount += 1


        for eachPoly in hitlist:
            self.polygon_accessor.SelectByIndex(eachPoly)
            if tagType in [MATERIAL, PART]:
                stringTag.Set(i_POLYTAG, replaceTag)

            elif tagType == PICK:
                pickTags = set(stringTag.Get(i_POLYTAG).split(";"))
                pickTags.discard(replaceTag)
                stringTag.Set(i_POLYTAG, ";".join(pickTags))

class CommandClass(tagger.CommanderClass):
    #_commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'default': tagger.MATERIAL,
                    'values_list_type': 'popup',
                    'values_list': tagger.POPUPS_TAGTYPES,
                    'flags': [],
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)

        hitcount = 0
        tagCounter = 0
        for pTag in tagger.scene.all_tags_by_type(i_POLYTAG):
            if not tagger.shadertree.get_masks( pTags = { pTag: i_POLYTAG }):
                mesh_editor = MeshEditorClass([tagType, pTag], [lx.symbol.f_MESHEDIT_POL_TAGS])
                mesh_editor.do_mesh_edit()
                hitcount += mesh_editor.hitcount

                tagCounter += 1

        try:
            modo.dialogs.alert(
                tagger.DIALOGS_UNTAGGED_POLYS_COUNT[0],
                tagger.DIALOGS_UNTAGGED_POLYS_COUNT[1] % (tagCounter, hitcount)
            )
        except:
            pass

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


lx.bless(CommandClass, CMD_NAME)
