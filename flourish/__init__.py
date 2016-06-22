import os

from .source import TomlSourceFile


class Flourish(object):
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self._source_files = []
        self._add_sources()

    @property
    def sources(self):
        return self

    def all(self):
        """ Get all source documents. """
        return self

    def count(self):
        """ Get the count of all source documents. """
        _sources = 0
        for source in self.sources.all():
            _sources += 1
        return _sources

    def get(self, slug):
        """ Get a single source document by slug. """
        for source in self.sources.all():
            if source.slug == slug:
                return source
        raise TomlSourceFile.DoesNotExist

    def _add_sources(self):
        """ Find source documents and register them. """
        trim = len(self.source_dir) + 1
        for root, dirs, files in os.walk(self.source_dir):
            this_dir = root[trim:]
            for file in files:
                if len(this_dir):
                    file = '%s/%s' % (this_dir, file)
                if file.endswith('.toml'):
                    self._source_files.append(TomlSourceFile(file))

    def __len__(self):
        return self.count()

    def __iter__(self):
        return iter(self._source_files)
