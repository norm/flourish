from glob import glob
import os
import warnings

import markdown2
import toml


class BaseSourceFile(object):
    def __init__(self, parent, filename):
        slug, _ = os.path.splitext(filename)
        self._source = filename
        self._slug = slug
        self._parent = parent
        self._config = self._read_configuration(filename)
        self._add_markdown_attachments()
        self._convert_markdown()

    @property
    def slug(self):
        return self._slug

    @property
    def url(self):
        return '/%s' % self._slug

    def _read_configuration(self, filename):
        toml_file = '%s/%s' % (self._parent.source_dir, filename)
        with open(toml_file) as configuration:
            return toml.loads(configuration.read())

    def _add_markdown_attachments(self):
        pattern = '%s/%s.*.markdown' % (self._parent.source_dir, self.slug)
        for attachment in glob(pattern):
            key = attachment.split('.')[-2] + '_markdown'
            with open(attachment) as content:
                if key in self._config:
                    warnings.warn(
                        '"%s" in %s overriden by attachment file.' % (
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
        raise AttributeError

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __iter__(self):
        _keys = self._config.keys()
        _keys.append('slug')
        return iter(_keys)

    def __repr__(self):
        return '<flourish.TomlSourceFile object (%s)>' % self._source

    class DoesNotExist(Exception):
        pass


class MarkdownSourceFile(BaseSourceFile):
    def _read_configuration(self, filename):
        markdown_file = '%s/%s' % (self._parent.source_dir, filename)
        with open(markdown_file) as configuration:
            content = configuration.read()
        if content.startswith('---\n'):
            # 4 skips the starting `---\n`; 8 skips both
            end = content[4:].find('---\n')
            if end != -1:
                # we have a TOML block
                config = toml.loads(content[4:end+4])
                config['body_markdown'] = content[end+8:]
            else:
                raise RuntimeError(
                    '"%s" has no end marker for the frontmatter' % filename
                )
        else:
            config = {}
            config['body_markdown'] = content
        return config


class TomlSourceFile(BaseSourceFile):
    pass
