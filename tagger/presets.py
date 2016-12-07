import lx
from os import listdir, sep
from os.path import isfile, join, basename, splitext, dirname

def string_beautify(string):
    return string.title().replace("_", " ")

def list_presets():
    presets_paths = [
        "kit_mecco_tagger:basics"
    ]

    raw_presets_list = []
    for path in presets_paths:
        presets_folder = lx.eval("query platformservice alias ? {%s}" % path)
        raw_presets_list += [join(presets_folder, f) for f in listdir(presets_folder) if isfile(join(presets_folder, f))]

    if not raw_presets_list:
        return []

    presets_list = []
    for p in raw_presets_list:
        nice_name = string_beautify(dirname(p).split(sep)[-1]) + " - "
        nice_name += string_beautify(splitext(basename(p))[0])
        internal_name = p
        presets_list.append((internal_name, nice_name))

    return presets_list
