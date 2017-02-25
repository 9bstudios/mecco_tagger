#python

import lx, lxu, modo, tagger, traceback

"""The TaggerPresetPaths() class contains a class variable with a list of
paths. We need to register our paths there in order for them to be used. It's
set up this way so that other kits can add themselves to Tagger simply by
importing tagger and running `tagger.TaggerPresetPaths().add_path(path)`"""

tagger.TaggerPresetPaths().add_path("kit_mecco_tagger:basics")

class CommandClass(tagger.CommanderClass):
    """We use a user value to store the user presets path. This is mainly out
    of laziness. A better way would be to create a query command that appends
    itself to the TaggerPresetPaths() class list. Oh well."""

    #_commander_default_values = []

    def commander_execute(self, msg, flags):
        target = modo.dialogs.dirBrowse(tagger.LABEL_CHOOSE_FOLDER)
        if target:
            lx.eval('user.value mecco_tagger.userPresetsPath {%s}' % target)

lx.bless(CommandClass, tagger.CMD_PREFS_SET_USER_PRESETS_PATH)
