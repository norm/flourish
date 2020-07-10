import re


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
    def get_current_path(self, tokens):
        self.current_path = self.resolve(**tokens)
        return self.current_path

    def resolve(self, **kwargs):
        resolved = ''
        # FIXME use self.arguments
        for segment in re.split(r'(#\w+)', self.path):
            if segment.startswith('#'):
                key = segment[1:]
                if key in kwargs:
                    if kwargs[key] is None:
                        raise RuntimeError
                    resolved = '%s%s' % (resolved, kwargs[key])
                else:
                    raise KeyError
            else:
                resolved = resolved + segment
        return resolved

    def can_generate(self, path):
        subpath = None
        if path.endswith('?'):
            subpath = path[:len(path)-1]
        generates = []
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
            filters = self.flourish.get_valid_filters_for_tokens(args)
            for _filter in filters:
                valid_filters.append(_filter)
        return valid_filters

    @property
    def arguments(self):
        arguments = []
        for segment in re.split(r'(#\w+)', self.path):
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


class TemplateMixin:
    def render_output(self):
        context = self.get_context_data()
        template = self.get_template()
        return self.render_template(template, context)

    def get_template(self):
        name = self.get_template_name()
        if name is None:
            raise MissingValue
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
            if 'type' in self.source_objects[0]:
                return '%s.html' % self.source_objects[0]['type']
        return super().get_template_name()
