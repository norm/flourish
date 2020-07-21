import hashlib
import json

from jinja2 import BaseLoader, TemplateNotFound
from sectile import Sectile


class SectileLoader(BaseLoader):
    def __init__(self, fragments_dir):
        self.sectile = Sectile(fragments=fragments_dir)
        self.prepared_path = None
        self.prepared_base = None
        self.prepared_dimensions = None
        self.contents = {}
        self.fragments = {}

    def dimensions(self):
        return self.sectile.get_dimensions_list()

    def prepare_template(self, path, base_template, **dimensions):
        self.prepared_path = path
        self.prepared_base = base_template
        self.prepared_dimensions = dimensions
        content, fragments = self.sectile.generate(
            path,
            base_template,
            **dimensions
        )
        fingerprint = '%s-%s-%s' % (
            path,
            base_template,
            json.dumps(dimensions)
        )
        digest = hashlib.sha256(fingerprint.encode('utf8')).hexdigest()
        self.contents[digest] = content
        self.fragments[digest] = fragments
        return digest

    def get_source(self, environment, digest):
        if self.contents[digest] is None:
            raise TemplateNotFound(
                "%s, %s {%s}" % (
                    self.prepared_path,
                    self.prepared_base,
                    self.prepared_dimensions
                )
            )
        else:
            return self.contents[digest], None, None
