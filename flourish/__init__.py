import collections
from operator import attrgetter
import os
import warnings

from .source import TomlSourceFile


class Flourish(object):
    _filters = []
    _order_by = []
    _slice = None
    _source_files = []

    ARGS = [
        'source_dir',
    ]
    DATA = [
        '_filters',
        '_order_by',
        '_slice',
        '_source_files',
    ]

    def __init__(self, source_dir='source', **kwargs):
        self.source_dir = source_dir

        if not os.path.isdir(self.source_dir):
            raise AttributeError(
                'source_dir "%s" must exist' % self.source_dir)

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

    def filter(self, **kwargs):
        _clone = self.clone()
        for _key, _value in kwargs.iteritems():
            _clone._filters.append((_key, _value))
        return _clone

    def order_by(self, *args):
        return self.clone(_order_by=args)

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
                    self._source_files.append(TomlSourceFile(self, file))

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

    def _get_filtered_sources(self):
        _sources = []
        for _source in self._source_files:
            _add = True
            if len(self._filters):
                for _filter in self._filters:
                    if '__' in _filter[0]:
                        _field, _operator = _filter[0].split('__', 2)
                    else:
                        _field, _operator = _filter[0], 'eq'
                    _operation = OPERATORS.get(_operator)
                    if _operation is None:
                        # FIXME write test and raise more useful error
                        raise RuntimeError
                    try:
                        _test = getattr(_source, _field)
                    except AttributeError:
                        _test = None

                    _result = _operation(_test, _filter[1])
                    if not _result:
                        _add = False
            if _add:
                _sources.append(_source)
        if self._slice is not None:
            _sources = _sources.__getitem__(self._slice)
        return _sources

    def __iter__(self):
        _sources = self._get_filtered_sources()
        for _order in self._order_by:
            if _order[0] == '-':
                _rev = True
                _attr = _order[1:]
            else:
                _rev = False
                _attr = _order
            try:
                _sources = sorted(
                    _sources, key=attrgetter(_attr), reverse=_rev)
            except AttributeError:
                warnings.warn(
                    'sorting sources by "%s" failed: '
                    'not all sources have that attribute' % _order
                )

        return iter(_sources)

    def __repr__(self):
        return '<flourish.Flourish object (source=%s)' % self.source_dir


def _equal_or_inside(value, test):
    if type(value) == list:
        return test in value
    else:
        return value == test


def _not_equal_or_inside(value, test):
    return not _equal_or_inside(value, test)


def _less_than(value, test):
    return value < test


def _less_than_or_equal_to(value, test):
    return value <= test


def _greater_than(value, test):
    return value > test


def _greater_than_or_equal_to(value, test):
    return value >= test


def _contains(value, test):
    try:
        if type(value) == list:
            for _v in value:
                if test in _v:
                    return True
            return False
        else:
            return test in value
    except TypeError:
        return False


def _excludes(value, test):
    return not _contains(value, test)


def _inside(value, test):
    return value in test


def _outside(value, test):
    return value not in test


def _set(value, test):
    return value is not None


def _unset(value, test):
    return value is None


OPERATORS = {
    'eq': _equal_or_inside,
    'neq': _not_equal_or_inside,
    'lt': _less_than,
    'lte': _less_than_or_equal_to,
    'gt': _greater_than,
    'gte': _greater_than_or_equal_to,
    'contains': _contains,
    'excludes': _excludes,
    'in': _inside,
    'notin': _outside,
    'set': _set,
    'unset': _unset,
}
