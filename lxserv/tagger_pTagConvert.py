# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_CONVERT

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.FROM_TAG_TYPE,
                    'label': tagger.LABEL_FROM_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': [],
                }, {
                    'name': tagger.TO_TAG_TYPE,
                    'label': tagger.LABEL_TO_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.PICK,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': []
                }
            ]

    def basic_Icon(self):
        if self.commander_arg_value(0) and self.commander_arg_value(1):
            if self.commander_arg_value(0) == tagger.MATERIAL and self.commander_arg_value(1) == tagger.PICK:
                return 'tagger.convertMaterialToSet'
            elif self.commander_arg_value(0) == tagger.PART and self.commander_arg_value(1) == tagger.PICK:
                return 'tagger.convertPartToSet'
            elif self.commander_arg_value(0) == tagger.MATERIAL and self.commander_arg_value(1) == tagger.PART:
                return 'tagger.convertMaterialToPart'
            elif self.commander_arg_value(0) == tagger.PART and self.commander_arg_value(1) == tagger.MATERIAL:
                return 'tagger.convertPartToMaterial'
            elif self.commander_arg_value(0) == tagger.PICK and self.commander_arg_value(1) == tagger.PART:
                return 'tagger.convertSetToPart'
            elif self.commander_arg_value(0) == tagger.PICK and self.commander_arg_value(1) == tagger.MATERIAL:
                return 'tagger.convertSetToMaterial'

        return 'tagger.pTagConvert'

    def basic_ButtonName(self):
        if self.commander_arg_value(0):
            label = []
            label.append(tagger.LABEL_CONVERT)
            if self.commander_arg_value(0):
                label.append(tagger.util.i_POLYTAG_to_label(self.commander_arg_value(0)))
            label.append(tagger.LABEL_TO)
            if self.commander_arg_value(1):
                label.append(tagger.util.i_POLYTAG_to_label(self.commander_arg_value(1)))
            else:
                label.append("...")
            return " ".join(label)

    def commander_execute(self, msg, flags):
        fromTagType = self.commander_arg_value(0)
        toTagType = self.commander_arg_value(1)

        tagger.selection.convert_tags(
            tagger.util.string_to_i_POLYTAG(fromTagType),
            tagger.util.string_to_i_POLYTAG(toTagType)
            )

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


lx.bless(CommandClass, CMD_NAME)
