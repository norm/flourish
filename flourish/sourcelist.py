from collections import defaultdict
from datetime import date, datetime, timezone
from operator import attrgetter
import warnings


class SourceList:
    ARGS = [
        'filters',
        'ordering',
        'slice',
        'future',
    ]

    def __init__(self, sources, **kwargs):
        self.sources = sources
        self.ordering = []
        self.filters = []
        self.slice = None
        self.future = True

        for arg in self.ARGS:
            if arg in kwargs:
                if kwargs[arg] is not None:
                    setattr(self, arg, kwargs[arg])

    def all(self):
        """ Get all source documents. """
        return self

    def count(self):
        return self.__len__()

    def filter(self, **kwargs):
        clone = self.clone()
        for key, value in kwargs.items():
            clone.filters.append((key, value))
        return clone

    def exclude(self, **kwargs):
        clone = self.clone()
        for key, value in kwargs.items():
            if '__' in key:
                field, operator = key.split('__', 2)
            else:
                field, operator = key, 'eq'
            new_operator = INVERSE_OPERATORS.get(operator)
            key = '%s__%s' % (field, new_operator)
            clone.filters.append((key, value))
        return clone

    def exclude_future(self):
        clone = self.clone()
        clone.filters.append(('published__lt', datetime.now(tz=timezone.utc)))
        return clone

    def order_by(self, *args):
        return self.clone(ordering=args)

    def clone(self, **kwargs):
        for arg in self.ARGS:
            value = getattr(self, arg)
            if type(value) == list:
                kwargs.setdefault(arg, value[:])
            else:
                kwargs.setdefault(arg, value)
        return type(self)(self.sources, **kwargs)

    def get_filtered_sources(self):
        sources = []
        for source in self.sources:
            add = True
            if 'published' in source and not self.future:
                if source['published'] > datetime.now(tz=timezone.utc):
                    add = False
            if len(self.filters):
                for filter in self.filters:
                    if not add:
                        # already filtered out by a previous filter
                        continue
                    if '__' in filter[0]:
                        field, operator = filter[0].split('__', 2)
                    else:
                        field, operator = filter[0], 'eq'
                    operation = OPERATORS.get(operator)
                    if operation is None:
                        # FIXME write test and raise more useful error
                        raise RuntimeError
                    is_date_filter = (
                        field in ['year', 'month', 'day'] and
                        'published' in source and
                        type(source['published'] == datetime)
                    )

                    try:
                        if is_date_filter:
                            test = '%02d' % getattr(
                                source['published'], field)
                        else:
                            test = getattr(source, field)
                    except AttributeError:
                        test = None

                    result = operation(test, filter[1])
                    if not result:
                        add = False
            if add:
                sources.append(source)
        return sources

    @property
    def publication_dates(self):
        def recursively_default_dict():
            return defaultdict(recursively_default_dict)

        _captured = recursively_default_dict()
        for _source in self.all():
            try:
                _date = getattr(_source, 'published')
                _captured[_date.year][_date.month][_date.day] = 1
            except AttributeError:
                pass

        _dates = []
        for _year in sorted(_captured):
            _months = []
            for _month in sorted(_captured[_year]):
                _days = []
                for _day in sorted(_captured[_year][_month]):
                    _days.append(date(_year, _month, _day))
                _months.append({
                    'month': date(_year, _month, 1),
                    'days': _days
                })
            _dates.append({'year': date(_year, 1, 1), 'months': _months})
        return _dates

    def __iter__(self):
        sources = self.get_filtered_sources()
        for order in self.ordering:
            if order.startswith('-'):
                rev = True
                attr = order[1:]
            else:
                rev = False
                attr = order
            try:
                sources = sorted(
                    sources,
                    key=attrgetter(attr),
                    reverse=rev
                )
            except AttributeError:
                warnings.warn(
                    'sorting sources by "%s" failed: '
                    'not all sources have that attribute' % order
                )

        if self.slice is not None:
            sources = sources.__getitem__(self.slice)
        return iter(sources)

    def __len__(self):
        _sources = 0
        for source in self:
            _sources += 1
        return _sources

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start
            stop = item.stop
            if start and start < 0:
                start = self.count() + start
            if stop and stop < 0:
                stop = self.count() + stop
            return self.clone(slice=slice(start, stop))
        if item < 0:
            item = self.count() + item
        iterator = iter(self)
        try:
            for i in range(0, item+1):
                obj = next(iterator)
        except StopIteration:
            raise IndexError(item)
        return obj
        return None


def _equal_or_inside(value, test):
    if type(value) == list:
        return test in value
    else:
        return value == test


def _not_equal_or_inside(value, test):
    return not _equal_or_inside(value, test)


def _less_than(value, test):
    try:
        return value < test
    except TypeError:
        return False


def _less_than_or_equal_to(value, test):
    try:
        return value <= test
    except TypeError:
        return False


def _greater_than(value, test):
    try:
        return value > test
    except TypeError:
        return False


def _greater_than_or_equal_to(value, test):
    try:
        return value >= test
    except TypeError:
        return False


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
INVERSE_OPERATORS = {
    'neq': 'eq',
    'eq': 'neq',
    'lt': 'gte',
    'lte': 'gt',
    'gt': 'lte',
    'gte': 'lt',
    'contains': 'excludes',
    'excludes': 'contains',
    'in': 'notin',
    'notin': 'in',
    'set': 'unset',
    'unset': 'set',
}
