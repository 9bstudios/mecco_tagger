import lx, lxu, traceback
from lxifc import UIValueHints
from operator import ior

ARG_NAME = 'name'
ARG_LABEL = 'label'
ARG_VALUE = 'value'
ARG_DATATYPE = 'datatype'
ARG_POPUP = 'popup'
ARG_FLAGS = 'flags'
ARG_sPresetText = 'sPresetText'

sTYPE_FLOATs = [
        'acceleration',
        'angle',
        'angle3',
        'axis',
        'float',
        'float3',
        'force',
        'fpixel',
        'light',
        'mass',
        'percent',
        'percent3',
        'speed',
        'time',
        'uvcoord'
    ]

sTYPE_STRINGs = [
        'color',
        'color1',
        'date',
        'datetime',
        'filepath',
        'string'
    ]

sTYPE_INTEGERs = [
        'integer',
        'intrange'
    ]

sTYPE_BOOLEANs = [
        'boolean'
    ]

class PopupClass(UIValueHints):
    def __init__(self, items):
        if not items or not isinstance(items, (list, tuple)):
            self._user = []
            self._internal = []

        elif isinstance(items[0], (list, tuple)):
            self._user = [str(i[1]) for i in items]
            self._internal = [str(i[0]) for i in items]

        else:
            self._user = [str(i) for i in items]
            self._internal = [str(i) for i in items]

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._internal)

    def uiv_PopUserName(self,index):
        return self._user[index]

    def uiv_PopInternalName(self,index):
        return self._internal[index]


class Commander(lxu.command.BasicCommand):
    _last_used = []
    _arguments = []

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        for n, argument in enumerate(self.commander_arguments()):
            self._last_used.append(argument[ARG_VALUE])
            self._arguments.append(argument)

            datatype = getattr(lx.symbol, 'sTYPE_' + argument[ARG_DATATYPE].upper())
            self.dyna_Add(argument[ARG_NAME], lx.symbol.sTYPE_STRING)

            flags = []
            for flag in argument[ARG_FLAGS]:
                flags.append(getattr(lx.symbol, 'fCMDARG_' + flag.upper()))

            if flags:
                self.basic_SetFlags(n, reduce(ior, flags))

    def commander_arguments(self):
        return []

    def commander_arg_value(self, index):
        return self._arguments[index][ARG_VALUE]

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        for n, argument in enumerate(self.commander_arguments()):
            if index == n:
                if ARG_LABEL in argument:
                    label = argument[ARG_LABEL]
                else:
                    label = argument[ARG_NAME]

                if ARG_sPresetText in argument:
                    hints.Class("sPresetText")

    def arg_UIValueHints(self, index):
        for n, argument in enumerate(self.commander_arguments()):
            if index == n and argument[ARG_POPUP]:
                return PopupClass(argument[ARG_POPUP])

    def cmd_DialogInit(self):
        for n, argument in enumerate(self.commander_arguments()):

            if argument[ARG_DATATYPE].lower() in sTYPE_STRINGs:
                self.attr_SetString(n, self._last_used[n])

            elif argument[ARG_DATATYPE].lower() in sTYPE_INTEGERs:
                self.attr_SetInt(n, self._last_used[n])

            elif argument[ARG_DATATYPE].lower() in sTYPE_BOOLEANs:
                self.attr_SetInt(n, self._last_used[n])

            elif argument[ARG_DATATYPE].lower in sTYPE_FLOATs:
                self.attr_SetFlt(n, self._last_used[n])

    @classmethod
    def set_last_used(cls, key, value):
        cls._last_used[key] = value

    @classmethod
    def set_argument(cls, key, value):
        cls._arguments[key] = value

    def commander_execute(self, msg, flags):
        pass

    def basic_Execute(self, msg, flags):
        try:
            for n, argument in enumerate(self.commander_arguments()):

                if argument[ARG_DATATYPE].lower() in sTYPE_STRINGs:
                    argument[ARG_VALUE] = self.dyna_String(n) if self.dyna_IsSet(n) else self._last_used[n]

                elif argument[ARG_DATATYPE].lower() in sTYPE_INTEGERs:
                    argument[ARG_VALUE] = self.dyna_Int(n) if self.dyna_IsSet(n) else self._last_used[n]

                elif argument[ARG_DATATYPE].lower in sTYPE_FLOATs:
                    argument[ARG_VALUE] = self.dyna_Float(n) if self.dyna_IsSet(n) else self._last_used[n]

                elif argument[ARG_DATATYPE].lower() in sTYPE_BOOLEANs:
                    argument[ARG_VALUE] = self.dyna_Bool(n) if self.dyna_IsSet(n) else self._last_used[n]

                self.set_last_used(n, argument[ARG_VALUE])
                self.set_argument(n, argument)

            self.commander_execute(msg, flags)

        except:
            lx.out(traceback.format_exc())

    # def cmd_Query(self,index,vaQuery):
    #     va = lx.object.ValueArray()
    #     va.set(vaQuery)
    #     for n, argument in enumerate(self.commander_arguments()):
    #         if index == n:
    #             va.AddString(self._last_used[1])
    #     return lx.result.OK
