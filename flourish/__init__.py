# encoding: utf8

from collections import defaultdict
from datetime import date, datetime
from importlib.machinery import SourceFileLoader
from operator import itemgetter
import os
from shutil import copyfile, rmtree
import sys
import warnings

from jinja2 import Environment, FileSystemLoader
import toml

from .lib import relative_list_of_files_in_directory
from .sectileloader import SectileLoader
from .source import (
    JsonSourceFile,
    MarkdownSourceFile,
    SourceFile,
    TomlSourceFile,
    CsvSourceFile,
)
from .sourcelist import SourceList
from .version import __version__    # noqa: F401

sys.dont_write_bytecode = True


class Flourish(object):
    def __init__(
        self,
        source_dir='source',
        templates_dir='templates',
        output_dir='output',
        sass_dir='sass',
        fragments_dir=None,
        future=None,
        skip_scan=False,
    ):
        self.source_dir = source_dir
        self.templates_dir = templates_dir
        self.fragments_dir = fragments_dir
        self.output_dir = output_dir
        self.sass_dir = sass_dir
        self.future = future
        self._assets = {}
        self._cache = {}
        self._source_files = []
        self._source_path = None
        self._paths = {}

        # using sectile fragments overrides standard filesystem templates
        if self.fragments_dir:
            self.using_sectile = True
            self.jinja = Environment(
                loader=SectileLoader(self.fragments_dir),
                keep_trailing_newline=True,
            )
        else:
            self.using_sectile = False
            self.jinja = Environment(
                loader=FileSystemLoader(self.templates_dir),
                keep_trailing_newline=True,
            )

        self.jinja.globals['path'] = self.template_resolve_path
        self.jinja.globals['lookup'] = self.template_get

        if not os.path.isdir(self.source_dir):
            raise Flourish.RuntimeError(
                'The source directory "%s" must exist' % self.source_dir)

        self.site_config = self._read_site_config()
        if not skip_scan:
            self._rescan_sources()

        try:
            generate = SourceFileLoader(
                    'generate', '%s/generate.py' % self.source_dir
                ).load_module()
        except FileNotFoundError:
            raise Flourish.RuntimeError(
                ('The source directory "%s"'
                 ' must contain the file "generate.py"')
                    % self.source_dir
            )

        try:
            self.set_global_context(getattr(generate, 'GLOBAL_CONTEXT'))
        except AttributeError:
            # global context is optional
            pass

        try:
            self.add_template_filters(getattr(generate, 'TEMPLATE_FILTERS'))
        except AttributeError:
            # filters are optional
            pass

        try:
            for path in generate.PATHS:
                self.add_path(path)
        except AttributeError:
            raise Flourish.RuntimeError(
                'There are no paths configured in generate.py')

    @property
    def sources(self):
        try:
            future = self.site_config['future'] 
        except KeyError:
            future = True

        # object instantiation takes precedence over site config
        if self.future is not None:
            future = self.future

        return SourceList(
            self._source_files,
            future = future
        )

    def get(self, slug):
        """ Get a single source document by slug. """
        try:
            return self._cache[slug]
        except KeyError:
            raise SourceFile.DoesNotExist

    def template_get(self, slug):
        try:
            return self.get(slug)
        except SourceFile.DoesNotExist:
            warnings.warn('Cannot get "%s" as it does not exist' % slug)
            return None

    def add_path(self, path):
        path.setup(self)
        if path.name == 'source':
            self._source_path = path
        if hasattr(path, 'required_config_keys'):
            for key in path.required_config_keys:
                if key not in self.site_config:
                    raise Flourish.MissingKey(
                        '%s requires an entry "%s" in _site.toml' % (
                            path.__class__.__name__,
                            key,
                        ))
        self._paths.update({path.name: path})

    def resolve_path(self, name, **kwargs):
        return self._paths[name].resolve(**kwargs)

    def template_resolve_path(self, name, **kwargs):
        try:
            return self.resolve_path(name, **kwargs)
        except KeyError:
            warnings.warn(
                'Cannot resolve path "%s", it has missing arguments' % name
            )
            return ''

    def get_handler_for_path(self, path):
        matches = []
        for key in self._paths:
            _dicts = self._paths[key].can_generate(path)
            if _dicts:
                for _dict in _dicts:
                    matches.append((key, _dict))
        return matches

    def all_valid_filters_for_path(self, name):
        if name in self._paths:
            return self._paths[name].all_valid_filters()
        else:
            raise SourceFile.DoesNotExist

    def generate_site(self, report=False):
        if os.path.exists(self.output_dir):
            rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        self.generate_all_paths(report=report)
        self.copy_assets(report=report)

    def generate_all_paths(self, report=False):
        for path in self._paths:
            self._paths[path].generate(report)

    def generate_path(self, path, report=False):
        handlers = self.get_handler_for_path(path)
        for key, args in handlers:
            path = self._paths[key]
            path.generate(report, tokens=[args])

    def path_recipe(self, path):
        handlers = self.get_handler_for_path(path)
        for key, args in handlers:
            path = self._paths[key]
            recipe = path.get_recipe(tokens=[args])
            if recipe:
                return recipe
        return None

    def set_global_context(self, global_context):
        self.global_context = global_context

    def add_template_filters(self, filters):
        for key, value in filters.items():
            self.jinja.filters[key] = value

    def copy_assets(self, report=False):
        for _file in self._assets:
            _source = '%s/%s' % (self.source_dir, _file)
            _destination = '%s/%s' % (self.output_dir, _file)
            _directory = os.path.dirname(_destination)
            if not os.path.isdir(_directory):
                os.makedirs(_directory)
            copyfile(_source, _destination)
            if report:
                print('++', _destination)

    def _read_site_config(self):
        _config_file = '%s/_site.toml' % self.source_dir
        try:
            with open(_config_file) as _file:
                return toml.loads(_file.read())
        except FileNotFoundError:
            return {}

    def _rescan_sources(self):
        """ Find source documents and register them. """
        _seen = {}
        for _file in relative_list_of_files_in_directory(self.source_dir):
            if _file == '_site.toml':
                continue
            if _file.startswith('generate.py'):
                continue
            slug, _ = os.path.splitext(_file)
            timestamp = os.stat(os.path.join(self.source_dir, _file)).st_mtime
            try:
                source = self.get(slug)
                assert timestamp == source.timestamp
                _seen[slug] = 1
            except:     # noqa: E722
                # FIXME check for slug-ishness and otherwise ignore
                # (this could simplify _site.toml by being just another
                # ignored filename?)
                is_attachment_file = (
                    _file.endswith(('.markdown', '.html')) and
                    len(_file.split('.')) == 3
                )

                if _file.endswith('.toml'):
                    self._cache[slug] = TomlSourceFile(self, _file)
                    _seen[slug] = 1
                elif (
                    _file.endswith('.markdown')
                    and len(_file.split('.')) == 2
                ):
                    self._cache[slug] = MarkdownSourceFile(self, _file)
                    _seen[slug] = 1
                elif _file.endswith('.json'):
                    self._cache[slug] = JsonSourceFile(self, _file)
                    _seen[slug] = 1
                elif _file.endswith('.csv'):
                    for src in CsvSourceFile(self, _file).get_sources():
                        if src['slug'] in _seen:
                            warnings.warn(
                                (
                                    'Existing source "%s" has been '
                                    'overriden by "%s"'
                                ) % (
                                    src['slug'],
                                    src,
                                )
                            )
                        self._cache[src['slug']] = src
                        _seen[src['slug']] = 1
                elif not is_attachment_file:
                    self._assets[_file] = True

        # remove anything no longer there
        # FIXME will also need output removing
        _removed = {}
        for source in self._cache:
            if source not in _seen:
                _removed[source] = 1
        for source in _removed:
            del self._cache[source]

        self._source_files = self._cache.values()

    @property
    def publication_dates(self):
        def recursively_default_dict():
            return defaultdict(recursively_default_dict)

        _captured = recursively_default_dict()
        for _source in self.sources.all():
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

    def get_valid_filters_for_tokens(self, tokens, objects=None):
        if objects is None:
            objects = self.sources

        _first_token = tokens[0]

        _values = set()
        for _source in objects:
            _is_date_filter = (
                _first_token in ['year', 'month', 'day'] and
                'published' in _source and
                type(_source['published'] == datetime)
            )

            if _is_date_filter:
                _value = getattr(_source['published'], _first_token)
                _values.add('%02d' % _value)
            elif _first_token in _source:
                if type(_source[_first_token]) == list:
                    for _value in _source[_first_token]:
                        _values.add(_value)
                else:
                    _values.add(_source[_first_token])

        _filters = []
        for _value in _values:
            _dict = {_first_token: _value}
            if len(tokens) == 1:
                _filters.append(_dict)
            else:
                _sub_objects = objects.filter(**_dict)
                _sub_tokens = self.get_valid_filters_for_tokens(
                    tokens[1:], _sub_objects)
                for _sub_token in _sub_tokens:
                    _update = _dict.copy()
                    _update.update(_sub_token)
                    _filters.append(_update)

        # the sort is only so the tests can compare results easily
        return sorted(_filters, key=itemgetter(_first_token))

    def __repr__(self):
        return '<flourish.Flourish object (source=%s)>' % self.source_dir


    class MissingKey(Exception):
        pass

    class RuntimeError(Exception):
        pass

