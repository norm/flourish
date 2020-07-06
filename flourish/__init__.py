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
from .source import (
    JsonSourceFile,
    MarkdownSourceFile,
    SourceFile,
    TomlSourceFile,
)
from .sourcelist import SourceList
from .url import URL
from .version import __version__    # noqa: F401

sys.dont_write_bytecode = True


class Flourish(object):
    ARGS = [
        'source_dir',
        'templates_dir',
        'output_dir',
        'sass_dir',
        'jinja',
    ]
    DATA = [
        '_assets',
        '_cache',
        '_source_files',
        '_source_url',
        '_urls',
    ]
    ACTIONS = [
        '_filters',
        '_order_by',
        '_slice',
    ]

    def __init__(
        self,
        source_dir='source',
        templates_dir='templates',
        output_dir='output',
        sass_dir='sass',
        global_context=None,
        **kwargs
    ):
        self.source_dir = source_dir
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        self.sass_dir = sass_dir
        self.global_context = global_context
        self.jinja = Environment(
            loader=FileSystemLoader(self.templates_dir),
            keep_trailing_newline=True,
            extensions=['jinja2.ext.with_'],
        )
        self.jinja.globals['url'] = self.template_resolve_url
        self.jinja.globals['lookup'] = self.template_get

        self._assets = {}
        self._cache = {}
        self._filters = []
        self._order_by = []
        self._slice = None
        self._source_files = []
        self._source_url = None
        self._urls = {}

        if not os.path.isdir(self.source_dir):
            raise AttributeError(
                'source_dir "%s" must exist' % self.source_dir)

        for _opt in self.DATA + self.ACTIONS:
            if _opt in kwargs:
                if kwargs[_opt] is not None:
                    setattr(self, _opt, kwargs[_opt])

        self.site_config = self._read_site_config()

        if '_source_files' not in kwargs:
            self._rescan_sources()

        generate = SourceFileLoader(
                'generate', '%s/generate.py' % self.source_dir
            ).load_module()

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

        has_urls = False
        try:
            self.canonical_source_url(*generate.SOURCE_URL)
            has_urls = True
        except AttributeError:
            # source URLs are optional
            pass

        try:
            for url in generate.URLS:
                has_urls = True
                self.add_url(*url)
        except NameError:
            # other URLs are optional
            pass

        if not has_urls:
            warnings.warn('There are no URLs configured in generate.py')

    @property
    def sources(self):
        return SourceList(self._source_files)

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

    def canonical_source_url(self, url, generator):
        # FIXME hmmmm
        self._source_url = URL(self, url, 'source', generator)
        self.add_url(url, 'source', generator)

    def add_url(self, url, name, generator):
        _url_dict = {name: URL(self, url, name, generator)}
        self._urls.update(_url_dict)

    def resolve_url(self, name, **kwargs):
        return self._urls[name].resolve(**kwargs)

    def template_resolve_url(self, name, **kwargs):
        try:
            return self.resolve_url(name, **kwargs)
        except KeyError:
            warnings.warn(
                'Cannot resolve URL "%s", it has missing arguments' % name
            )
            return ''

    def get_handler_for_path(self, path):
        matches = []
        for key in self._urls:
            _dicts = self._urls[key].can_generate(path)
            if _dicts:
                for _dict in _dicts:
                    matches.append((key, _dict))
        return matches

    def all_valid_filters_for_url(self, name):
        if name in self._urls:
            return self._urls[name].all_valid_filters()
        else:
            raise URL.DoesNotExist

    def generate_site(self, report=False):
        if os.path.exists(self.output_dir):
            rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        self.generate_all_urls(report=report)
        self.copy_assets(report=report)
        if report:
            print('')

    def generate_all_urls(self, report=False):
        for _entry in self._urls:
            self.generate_url(_entry, report=report)

    def generate_url(self, name, report=False):
        url = self._urls[name]
        url.generator(self, url, self.global_context, report=report)

    def generate_path(self, path, report=False):
        handlers = self.get_handler_for_path(path)
        for key, args in handlers:
            url = self._urls[key]
            url.generator(
                self,
                url,
                self.global_context,
                report=report,
                tokens=[args],
            )

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
                print('->', _destination)

    def _read_site_config(self):
        _config_file = '%s/_site.toml' % self.source_dir
        with open(_config_file) as _file:
            _config = toml.loads(_file.read())
        for key in ('author', 'title', 'base_url'):
            if key not in _config:
                raise RuntimeError(
                    '"%s" is a required entry in _site.toml' % key)
        return _config

    def _rescan_sources(self):
        """ Find source documents and register them. """
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
                elif (
                    _file.endswith('.markdown')
                    and len(_file.split('.')) == 2
                ):
                    self._cache[slug] = MarkdownSourceFile(self, _file)
                elif _file.endswith('.json'):
                    self._cache[slug] = JsonSourceFile(self, _file)
                elif not is_attachment_file:
                    self._assets[_file] = True
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
