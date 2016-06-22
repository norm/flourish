import os


class TomlSourceFile(object):
    def __init__(self, filename):
        slug, _ = os.path.splitext(filename)
        self._source = filename
        self._slug = slug

    @property
    def slug(self):
        return self._slug

    class DoesNotExist(Exception):
        pass
