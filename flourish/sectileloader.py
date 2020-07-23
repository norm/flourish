import json

from jinja2 import BaseLoader, TemplateNotFound
from sectile import Sectile


class SectileLoader(BaseLoader):
    def __init__(self, fragments_dir):
        self.sectile = Sectile(fragments=fragments_dir)
        self.prepared_path = None
        self.prepared_base = None
        self.prepared_dimensions = None
        self.cache = {}

    def dimensions(self):
        return self.sectile.get_dimensions_list()

    def generate_template(self, path, base_template, **dimensions):
        fingerprint = '%s-%s-%s' % (
            path,
            base_template,
            json.dumps(dimensions)
        )
        content, fragments = self.sectile.generate(
            path,
            base_template,
            **dimensions
        )
        self.cache = {
            'path': path,
            'fingerprint': fingerprint,
            'base_template': base_template,
            'dimensions': dimensions,
            'content': content,
            'fragments': fragments,
        }
        return self.cache

    def prepare_template(self, path, base_template, **dimensions):
        generated = self.generate_template(path, base_template, **dimensions)
        return generated['fingerprint']

    def get_source(self, environment, fingerprint):
        if self.cache['fingerprint'] != fingerprint:
            raise TemplateNotFound(
                "%s, %s {%s}" % (
                    self.prepared_path,
                    self.prepared_base,
                    self.prepared_dimensions
                )
            )
        else:
            return self.cache['content'], None, None
