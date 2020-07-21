from collections import OrderedDict
import hashlib
import json

from jinja2 import BaseLoader, TemplateNotFound
from sectile import Sectile




class SectileLoader(BaseLoader):
    CACHE_SIZE=100

    def __init__(self, fragments_dir):
        self.sectile = Sectile(fragments=fragments_dir)
        self.prepared_path = None
        self.prepared_base = None
        self.prepared_dimensions = None
        # FIXME LRU cache, not everything ever
        self.cache = OrderedDict()

    def dimensions(self):
        return self.sectile.get_dimensions_list()

    def generate_template(self, path, base_template, **dimensions):
        fingerprint = '%s-%s-%s' % (
            path,
            base_template,
            json.dumps(dimensions)
        )
        # print('==', fingerprint)
        if fingerprint in self.cache:
            print('** cache hit')
            self.cache.move_to_end(fingerprint, last=True)
        else:
            # print('++ cache miss')
            content, fragments = self.sectile.generate(
                path,
                base_template,
                **dimensions
            )
            self.cache[fingerprint] = {
                'path': path,
                'fingerprint': fingerprint,
                'base_template': base_template,
                'dimensions': dimensions,
                'content': content,
                'fragments': fragments,
            }
        if len(self.cache) > self.CACHE_SIZE:
            # print('-- evict cache key')
            self.cache.popitem(last=False)

        return self.cache[fingerprint]

    def prepare_template(self, path, base_template, **dimensions):
        generated = self.generate_template(path, base_template, **dimensions)
        return generated['fingerprint']

    def get_source(self, environment, fingerprint):
        if self.cache[fingerprint] is None:
            raise TemplateNotFound(
                "%s, %s {%s}" % (
                    self.prepared_path,
                    self.prepared_base,
                    self.prepared_dimensions
                )
            )
        else:
            return self.cache[fingerprint]['content'], None, None
