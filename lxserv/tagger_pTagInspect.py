#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_PTAG_INSPECT

class CMD_tagger(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        tags = {
            tagger.MATERIAL:set(),
            tagger.PART:set(),
            tagger.PICK:set()
        }

        for layer in tagger.items.get_active_layers():
            with layer.geometry as geo:
                polys = geo.polygons.selected

                for p in polys:
                    if p.tags()[tagger.MATERIAL]:
                        tags[tagger.MATERIAL].add(p.tags()[tagger.MATERIAL])
                    if p.tags()[tagger.PART]:
                        tags[tagger.PART].add(p.tags()[tagger.PART])
                    if p.tags()[tagger.PICK]:
                        tags[tagger.PICK] = tags[tagger.PICK].union(set(p.tags()[tagger.PICK].split(";")))

        output = ""
        for tagType in tags:
            output += tagType + ": "
            if tags[tagType]:
                output += ", ".join(tags[tagType]) + "\n"
            else:
                output += tagger.LABEL_NONE + "\n"

        modo.dialogs.alert(tagger.LABEL_TAGS, output)



lx.bless(CMD_tagger, NAME_CMD)
