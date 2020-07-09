import os

import sass

from flourish.generators.base import BaseGenerator


# FIXME
# when refreshing sources, also refresh generators
class SassGenerator(BaseGenerator):
    output_style = 'expanded'
    file_extension = '.css'
    sass_sources = []

    def setup(self, flourish):
        super().setup(flourish)
        self.find_sass_sources()

    def find_sass_sources(self):
        for root, dirs, files in os.walk(self.flourish.sass_dir):
            root = root[len(self.flourish.sass_dir):]
            for file in files:
                base, ext = os.path.splitext(file)
                if not base.startswith('_') and ext == '.scss':
                    self.sass_sources.append(os.path.join(root, base))

    def get_path_tokens(self):
        tokens = []
        for source in self.sass_sources:
            tokens.append({'sass_source': source})
        return tokens

    def all_valid_filters(self):
        valid_filters = []
        args = self.arguments

        if len(args) == 0:
            valid_filters.append({})
        elif args == ['sass_source']:
            for source in self.sass_sources:
                valid_filters.append({'sass_source': source})
        else:
            raise ValueError
        return valid_filters

    def get_objects(self, tokens):
        # there are no Source objects
        pass

    def render_output(self):
        source = os.path.join(
            self.flourish.sass_dir,
            '%s.scss' % self.tokens['sass_source'],
        )
        return sass.compile(
            filename=source,
            output_style=self.output_style,
        )
