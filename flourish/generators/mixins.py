import os
import re

from sectile import Sectile


class MissingValue(Exception):
    pass


class ContextMixin:
    def get_context_data(self):
        context = {}
        context['site'] = self.flourish.site_config
        context['global'] = self.flourish.global_context(self.flourish)
        context['tokens'] = self.tokens
        if self.context:
            context.update(**self.context)
        return context


class PathMixin:
    PATH_SEGMENTS = r'(#\w+)'
    STRIP_PATH = r'^[\w_-]+'

    def get_current_path(self, tokens):
        self.current_path = self.resolve(**tokens)
        return self.current_path

    def resolve(self, **kwargs):
        resolved = ''
        # FIXME use self.arguments
        for segment in re.split(self.PATH_SEGMENTS, self.path):
            if segment.startswith('#'):
                key = segment[1:]
                if key in kwargs:
                    if kwargs[key] is None:
                        raise RuntimeError
                    if key == 'month' or key == 'day':
                        resolved = '%s%02d' % (resolved, int(kwargs[key]))
                    else:
                        resolved = '%s%s' % (resolved, kwargs[key])
                else:
                    raise KeyError
            else:
                resolved = resolved + segment
        return resolved

    def can_generate(self, path):
        subpath = None
        if path.endswith('?'):
            subpath = path[:-1]
        generates = []

        # see if the path can be rejected before continuing to the
        # expensive check-all-possible-matches, by checking if each
        # non-token part of the requested path is found in our path
        check_path = path
        segments = re.split(self.PATH_SEGMENTS, self.path)
        while len(segments) > 1:
            pos = check_path.find(segments[0])
            if pos < 0:
                return []
            check_path = check_path[(pos + len(segments[0])):]
            stripped = re.split(self.STRIP_PATH, check_path)
            if len(stripped) > 1:
                check_path = stripped[1]
            segments.pop(0)
            segments.pop(0)
        if check_path.endswith('?'):
            if segments[0].find(check_path[:-1]) < 0:
                return []
        elif not check_path.endswith(segments[0]):
            return []

        for _filter in self.all_valid_filters():
            filter_path = self.resolve(**_filter)
            if path == filter_path:
                generates.append(_filter)
            elif subpath and filter_path.startswith(subpath):
                generates.append(_filter)
        return generates

    def all_valid_filters(self):
        valid_filters = []
        args = self.arguments

        if len(args) == 0:
            valid_filters.append({})
        else:
            filters = self.flourish.get_valid_filters_for_tokens(
                args,
                self.get_filtered_sources(),
            )
            for _filter in filters:
                valid_filters.append(_filter)
        return valid_filters

    @property
    def arguments(self):
        arguments = []
        for segment in re.split(self.PATH_SEGMENTS, self.path):
            if segment.startswith('#'):
                arguments.append(segment[1:])
        return arguments

    def get_context_data(self):
        context = super().get_context_data()
        context['current_path'] = self.current_path
        return context


class SourcesMixin:
    order_by = None
    sources_exclude = None
    sources_filter = None
    limit = None

    def get_objects(self, tokens):
        sources = self.get_filtered_sources().filter(**tokens)
        ordering = self.get_order_by()
        if ordering is not None:
            sources = sources.order_by(self.order_by)
        if self.limit is not None:
            self.source_objects = sources[0:self.limit]
        else:
            self.source_objects = sources
        return self.source_objects

    def get_filtered_sources(self):
        sources = self.flourish.sources
        if self.sources_filter is not None:
            sources = sources.filter(**self.sources_filter)
        if self.sources_exclude is not None:
            sources = sources.exclude(**self.sources_exclude)
        return sources

    def get_order_by(self):
        return self.order_by

    def get_context_data(self):
        context = super().get_context_data()
        context['sources'] = self.source_objects
        return context


class GeneratorMixin:
    def generate(self, report=False, tokens=None):
        self.report = report
        if not tokens:
            tokens = self.get_path_tokens()
        for tokenset in tokens:
            self.tokens = tokenset
            self.generate_path(tokenset)

    def get_path_tokens(self):
        return self.flourish.all_valid_filters_for_path(self.name)

    def generate_path(self, tokens):
        self.get_current_path(tokens)
        self.get_objects(tokens)
        self.output_to_file()

    def get_recipe(self, tokens):
        for tokenset in tokens:
            self.tokens = tokenset
            self.get_current_path(tokenset)
            self.get_objects(tokenset)
            context = self.get_context_data()
            name = self.get_template_name()
            recipe = {
                'path': self.current_path,
                'context': context,
                'template_name': name,
            }
            if self.flourish.using_sectile:
                sectile = Sectile(fragments=self.flourish.fragments_dir)
                dimensions = {
                    'generator': self.name,
                }
                for dimension in self.flourish.jinja.loader.dimensions():
                    if dimension in context:
                        dimensions[dimension] = context[dimension]
                recipe['template'], recipe['sectile_fragments'] = sectile.generate(
                    self.current_path,
                    name,
                    **dimensions
                )
                recipe['sectile_dimensions'] = dimensions
            else:
                filename = os.path.join(self.flourish.templates_dir, name)
                with open(filename, 'r') as handle:
                    recipe['template'] = handle.read()
            return recipe


class TemplateMixin:
    def render_output(self):
        context = self.get_context_data()
        template = self.get_template(context)
        return self.render_template(template, context)

    def get_template(self, context):
        name = self.get_template_name()
        if name is None:
            raise MissingValue
        if self.flourish.using_sectile:
            # Sectile templates need to be constructed rather than just found
            # on the filesystem. Because the entrypoint to the jinja loader
            # doesn't allow any extra context than the name of the template to
            # be passed, we pre-construct and cache a template and then use
            # that cached value as the template's "name".
            dimensions = {
                'generator': self.name,
            }
            for dimension in self.flourish.jinja.loader.dimensions():
                if dimension in context:
                    dimensions[dimension] = context[dimension]
            digest = self.flourish.jinja.loader.prepare_template(
                self.current_path,
                name,
                **dimensions,
            )
            return self.flourish.jinja.get_template(digest)
        else:
            return self.flourish.jinja.get_template(name)

    def get_template_name(self):
        return self.template_name

    def render_template(self, template, context_data):
        return template.render(context_data)


class PageTemplateMixin:
    template_name = 'page.html'

    def get_template_name(self):
        if self.source_objects:
            if 'template' in self.source_objects[0]:
                return self.source_objects[0]['template']
            if 'page_type' in self.source_objects[0]:
                return '%s.html' % self.source_objects[0]['page_type']
        return super().get_template_name()
