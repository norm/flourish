import codecs
from datetime import datetime, timezone
from glob import glob
import json
import os
import re
import warnings

import markdown2
import toml


class SourceFile(object):
    def __init__(self, parent, filename):
        slug, _ = os.path.splitext(filename)
        self._source = filename
        self._slug = slug
        self._parent = parent
        self._config = self._read_configuration(filename)
        self._timestamp = os.stat(
                os.path.join(self._parent.source_dir, filename)
            ).st_mtime
        self._add_markdown_attachments()
        self._add_html_attachments()
        self._convert_markdown()

    @property
    def slug(self):
        return self._slug

    @property
    def path(self):
        # FIXME when _source_url is not set
        _path = self._parent._source_path
        _filter = {}
        for _arg in _path.arguments:
            try:
                _value = getattr(self, _arg)
                if type(_value) == list:
                    _filter[_arg] = _value[0]
                else:
                    _filter[_arg] = _value
            except AttributeError:
                warnings.warn(
                    'cannot create URL for "%s": no value for "%s"' % (
                        self._slug, _arg)
                )
                return None
        _resolved = _path.resolve(**_filter)
        if _resolved.endswith('/index'):
            _resolved = _resolved[:-5]
        return _resolved

    @property
    def absolute_url(self):
        return '%s%s' % (self._parent.site_config['base_url'], self.path)

    @property
    def timestamp(self):
        return self._timestamp

    def related(self, key):
        try:
            _filter = {}
            _filter[key] = self._config[key]
            return self._parent.sources.filter(
                    **_filter
                ).exclude(
                    slug=self.slug
                )
        except KeyError:
            return []

    def _read_configuration(self, filename):
        toml_file = '%s/%s' % (self._parent.source_dir, filename)
        with codecs.open(toml_file, encoding='utf-8') as configuration:
            return toml.loads(configuration.read())

    def _add_html_attachments(self):
        pattern = '%s/%s.*.html' % (self._parent.source_dir, self.slug)
        for attachment in glob(pattern):
            key = attachment.split('.')[-2]
            with codecs.open(attachment, encoding='utf-8') as content:
                if key in self._config:
                    warnings.warn(
                        '"%s" in %s overriden by HTML attachment.' % (
                            key, self.slug))
                self._config[key] = content.read()

    def _add_markdown_attachments(self):
        pattern = '%s/%s.*.markdown' % (self._parent.source_dir, self.slug)
        for attachment in glob(pattern):
            key = attachment.split('.')[-2] + '_markdown'
            with codecs.open(attachment, encoding='utf-8') as content:
                if key in self._config:
                    warnings.warn(
                        '"%s" in %s overriden by Markdown attachment.' % (
                            key, self.slug))
                self._config[key] = content.read()

    def _convert_markdown(self):
        add = {}
        for key in self._config:
            if key[-9:] == '_markdown':
                dest = key[:-9]
                add[dest] = markdown2.markdown(self._config[key])
                if dest in self._config:
                    warnings.warn(
                        '"%s" in %s overriden by Markdown conversion.' % (
                            dest, self.slug))
        self._config.update(add)

    def __getattr__(self, key):
        if key == 'slug':
            return self.slug
        if key in self._config:
            return self._config[key]

        # foreign key lookup
        _fkey = '%s_fkey' % key
        if _fkey in self._config:
            return self._parent.get(self._config[_fkey])

        # foreign key reverse lookup
        if key.endswith('_set'):
            _fkey = '%s_fkey' % key[:-4]
            _filter = {_fkey: self.slug}
            return self._parent.sources.filter(**_filter)

        if key in ['body', 'title']:
            # these are required for atom feeds, so if they've not been
            # set in the page's configuration, return them as empty
            return ''
        raise AttributeError

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __iter__(self):
        _keys = list(self._config)
        _keys.append('slug')
        return iter(_keys)

    def __repr__(self):
        return '<flourish.TomlSourceFile object (%s)>' % self._source

    class DoesNotExist(Exception):
        pass


class MarkdownSourceFile(SourceFile):
    def _read_configuration(self, filename):
        markdown_file = '%s/%s' % (self._parent.source_dir, filename)
        with codecs.open(markdown_file, encoding='utf-8') as configuration:
            content = configuration.read()
        if content.startswith('-') or content.startswith('`'):
            _delim_char = content[0:1]
            FM_SPLIT = re.compile('^%s{3}$' % _delim_char, re.MULTILINE)
            try:
                _, _frontmatter, _body = FM_SPLIT.split(content, 2)
                config = toml.loads(_frontmatter)
                config['body_markdown'] = _body
            except ValueError:
                raise RuntimeError(
                    '"%s" has no end marker for the frontmatter' % filename
                )
        else:
            config = {}
            config['body_markdown'] = content
        return config


class TomlSourceFile(SourceFile):
    pass


class JsonSourceFile(SourceFile):
    ISO8601 = re.compile(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}Z$')

    def _read_configuration(self, filename):
        _json_file = '%s/%s' % (self._parent.source_dir, filename)
        with codecs.open(_json_file, encoding='utf-8') as _configuration:
            _config = json.loads(_configuration.read())

        for _key, _value in _config.items():
            if type(_value) == str and self.ISO8601.match(_value):
                _config[_key] = datetime.strptime(
                        _value, "%Y-%m-%dT%H:%M:%SZ"
                    ).replace(tzinfo=timezone.utc)
        return _config
