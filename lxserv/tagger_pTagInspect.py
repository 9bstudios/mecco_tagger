#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = 'tagger.pTagInspect'

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
            "material":set(),
            "part":set(),
            "pick":set()
        }

        for layer in tagger.items.get_active_layers():
            with layer.geometry as geo:
                polys = geo.polygons.selected

                for p in polys:
                    if p.tags()["material"]:
                        tags["material"].add(p.tags()["material"])
                    if p.tags()["part"]:
                        tags["part"].add(p.tags()["part"])
                    if p.tags()["pick"]:
                        tags["pick"] = tags["pick"].union(set(p.tags()["pick"].split(";")))

        output = ""
        for tagType in tags:
            output += tagType + ": "
            if tags[tagType]:
                output += ", ".join(tags[tagType]) + "\n"
            else:
                output += "(none)\n"

        modo.dialogs.alert("Tags", output)



lx.bless(CMD_tagger, NAME_CMD)
