# python

class TaggerPresetPaths(object):
    _preset_paths = []

    def __init__(self):
        pass

    @classmethod
    def add_path(cls, path):
        """An array of preset paths that will be appended to the Tagger material
        preset popup."""
        cls._preset_paths.append(path)

    def paths():
        doc = "Returns the list of registered search paths."
        def fget(self):
            return self._preset_paths
        return locals()

    paths = property(**paths())
