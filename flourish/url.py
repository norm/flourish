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
        for _segment in re.split(r'(#\w+)', self.path):
            if _segment.startswith('#'):
                _arguments.append(_segment[1:])
        return _arguments

    def resolve(self, **kwargs):
        _resolved = ''
        for _segment in re.split(r'(#\w+)', self.path):
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

    def can_generate(self, path):
        subpath = None
        if path.endswith('?'):
            subpath = path[:len(path)-1]
        generates = []
        for _dict in self.all_valid_filters():
            x = self.resolve(**_dict)
            if path == x:
                generates.append(_dict)
            if subpath and x.startswith(subpath):
                generates.append(_dict)
        return generates

    def all_valid_filters(self):
        _valid_filters = []
        _args = self.arguments

        if len(_args) == 0:
            _valid_filters.append({})
        else:
            _filters = self.parent.copy().get_valid_filters_for_tokens(_args)
            for _dict in _filters:
                _valid_filters.append(_dict)
        return _valid_filters

    def __repr__(self):
        return '<flourish.URL object (%s: %s)>' % (self.name, self.path)

    class DoesNotExist(Exception):
        pass
