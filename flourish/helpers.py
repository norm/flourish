# encoding: utf8


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
