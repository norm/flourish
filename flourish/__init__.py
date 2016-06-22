import collections
import os

from .source import TomlSourceFile


class Flourish(object):
    _slice = None
    _source_files = []

    ARGS = [
        'source_dir',
    ]
    DATA = [
        '_slice',
        '_source_files',
    ]

    def __init__(self, source_dir='source', **kwargs):
        self.source_dir = source_dir

        for _opt in self.DATA:
            if _opt in kwargs:
                if kwargs[_opt] is not None:
                    setattr(self, _opt, kwargs[_opt])

        if '_source_files' not in kwargs:
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

    def clone(self, **kwargs):
        for _option in self.ARGS + self.DATA:
            _value = getattr(self, _option)
            if isinstance(_value, collections.Iterable):
                kwargs.setdefault(_option, _value[:])
            else:
                kwargs.setdefault(_option, _value)
        return type(self)(**kwargs)

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

    def __getitem__(self, item):
        if isinstance(item, slice):
            if (item.start < 0) or (item.stop < 0):
                raise ValueError('Cannot use negative indexes with Flourish')
            return self.clone(_slice=item)
        if item < 0:
            raise ValueError('Cannot use negative indexes with Flourish')
        _iterator = iter(self)
        try:
            for i in range(0, item+1):
                obj = next(_iterator)
        except StopIteration:
            raise IndexError(item)
        return obj
        return None

    def __iter__(self):
        _filtered = []
        for page in self._source_files:
            _filtered.append(page)
        if self._slice is not None:
            _filtered = _filtered.__getitem__(self._slice)
        return iter(_filtered)
