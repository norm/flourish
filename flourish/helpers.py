# encoding: utf8

from collections import defaultdict


def all_valid_dates(flourish, key='published'):
    def recursively_default_dict():
        return defaultdict(recursively_default_dict)

    _captured = recursively_default_dict()
    for _source in flourish.sources.all():
        try:
            _date = getattr(_source, key)
            _captured[_date.year][_date.month][_date.day] = 1
        except AttributeError:
            pass

    _dates = []
    for _year in sorted(_captured):
        _months = []
        for _month in sorted(_captured[_year]):
            _days = []
            for _day in sorted(_captured[_year][_month]):
                _days.append({'day': '%02d' % _day})
            _months.append({'month': '%02d' % _month, 'days': _days})
        _dates.append({'year': '%04d' % _year, 'months': _months})
    return _dates


def publication_range(flourish, key='published'):
    _lowest = None
    _highest = None

    for _source in flourish.sources.all():
        try:
            _pub = getattr(_source, key)
            _year = _pub.year
            if _lowest is None or _year < _lowest:
                _lowest = _year
            if _highest is None or _year > _highest:
                _highest = _year
        except AttributeError:
            pass

    if _lowest is not None and _highest is not None:
        return u'%d–%d' % (_lowest, _highest)
