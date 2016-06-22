import os

import toml


class TomlSourceFile(object):
    def __init__(self, parent, filename):
        slug, _ = os.path.splitext(filename)
        self._source = filename
        self._slug = slug
        self._parent = parent
        self._config = self._read_toml(filename)

    @property
    def slug(self):
        return self._slug

    def _read_toml(self, filename):
        toml_file = '%s/%s' % (self._parent.source_dir, filename)
        with open(toml_file) as configuration:
            return toml.loads(configuration.read())

    def __getattr__(self, key):
        if key in self._config:
            return self._config[key]
        raise AttributeError

    class DoesNotExist(Exception):
        pass
