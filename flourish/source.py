from glob import glob
import os
import warnings

import markdown2
import toml


class TomlSourceFile(object):
    def __init__(self, parent, filename):
        slug, _ = os.path.splitext(filename)
        self._source = filename
        self._slug = slug
        self._parent = parent
        self._config = self._read_toml(filename)
        self._add_markdown_attachments()
        self._convert_markdown()

    @property
    def slug(self):
        return self._slug

    def _read_toml(self, filename):
        toml_file = '%s/%s' % (self._parent.source_dir, filename)
        with open(toml_file) as configuration:
            return toml.loads(configuration.read())

    def _add_markdown_attachments(self):
        pattern = '%s/%s.*.markdown' % (self._parent.source_dir, self.slug)
        for attachment in glob(pattern):
            key = attachment.split('.')[-2] + '_markdown'
            with open(attachment) as content:
                print '**', attachment, key, self._config
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
        if key in self._config:
            return self._config[key]
        raise AttributeError

    def __repr__(self):
        return '<flourish.TomlSourceFile object (%s)>' % self._source

    class DoesNotExist(Exception):
        pass
