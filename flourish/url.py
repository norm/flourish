import re


class URL(object):
    def __init__(self, parent, path, name, generator):
        self.parent = parent
        self.path = path
        self.name = name
        self.generator = generator

    @property
    def arguments(self):
        _arguments = []
        for _segment in re.split('(#\w+)', self.path):
            if _segment.startswith('#'):
                _arguments.append(_segment[1:])
        return _arguments

    def resolve(self, **kwargs):
        _resolved = ''
        for _segment in re.split('(#\w+)', self.path):
            if _segment.startswith('#'):
                key = _segment[1:]
                if key in kwargs:
                    if kwargs[key] is None:
                        raise RuntimeError
                    _resolved = _resolved + kwargs[key]
                else:
                    raise KeyError
            else:
                _resolved = _resolved + _segment
        return _resolved

    def all_valid_filters(self):
        _valid_filters = []
        _args = self.arguments

        if len(_args) == 0:
            _valid_filters.append({})
        else:
            _filters = self.get_all_filters_for_arguments(_args)
            for _dict in _filters:
                _valid_filters.append(_dict)
        return _valid_filters

    def get_all_filters_for_arguments(self, keys, objects=None):
        if objects is None:
            objects = self.parent

        _first_key = keys[0]

        _values = set()
        for _source in objects:
            if _first_key in _source:
                if type(_source[_first_key]) == list:
                    for _value in _source[_first_key]:
                        _values.add(_value)
                else:
                    _values.add(_source[_first_key])

        _filters = []
        for _value in _values:
            _dict = {_first_key: _value}
            if len(keys) == 1:
                _filters.append(_dict)
            else:
                _sub_objects = objects.filter(**_dict)
                _sub_keys = self.get_all_filters_for_arguments(
                    keys[1:], _sub_objects)
                for _sub_key in _sub_keys:
                    _update = _dict.copy()
                    _update.update(_sub_key)
                    _filters.append(_update)

        # the sort is only so the tests can compare results easily
        return sorted(_filters)

    def __repr__(self):
        return '<flourish.URL object (%s: %s)>' % (self.name, self.path)
