import os

from .mixins import (
    PathMixin,
    SourcesMixin,
    GeneratorMixin,
    ContextMixin,
    TemplateMixin,
    PageTemplateMixin,
)
from ..paginator import Paginator


class BaseGenerator(ContextMixin, PathMixin, GeneratorMixin, TemplateMixin):
    """
    The BaseGenerator takes care of the interface with Flourish.
    """
    def __init__(self, path, name, context={}):
        self.path = path
        self.name = name
        self.context = context

    def setup(self, flourish):
        self.flourish = flourish

    def output_to_file(self):
        filename = self.get_output_filename()
        if self.report:
            print('->', filename)

        rendered = self.render_output()
        directory = os.path.dirname(filename)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        with open(filename, 'w', encoding='utf8') as output:
            output.write(rendered)

    def get_output_filename(self):
        destination = '%s%s' % (self.flourish.output_dir, self.current_path)
        if destination.endswith('/'):
            destination = destination + 'index.html'
        if not destination.endswith(self.file_extension):
            destination = destination + '.html'
        return destination


class StaticGenerator(BaseGenerator):
    file_extension = '.html'

    def get_objects(self, tokens):
        self.source_objects = []
        return []


class SourceGenerator(SourcesMixin, PageTemplateMixin, BaseGenerator):
    template_name = 'page.html'
    file_extension = '.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['page'] = self.source_objects[0]
        context.update(self.source_objects[0]._config)
        return context


class IndexGenerator(SourcesMixin, BaseGenerator):
    template_name = 'index.html'
    file_extension = '.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['pages'] = self.source_objects
        return context


class PaginatedIndexGenerator(IndexGenerator):
    per_page = 10

    def generate_path(self, tokens):
        path = self.get_current_path(tokens)
        paginator = self.get_paginated_objects(tokens, path)
        for page in paginator:
            self.current_path = page.path
            self.source_objects = page.object_list
            self.current_page = page
            self.output_to_file()

    def get_paginated_objects(self, tokens, path):
        objects = self.get_objects(tokens)
        per_page = self.get_per_page()
        self.paginator = Paginator(objects, per_page, path)
        return self.paginator

    def get_per_page(self):
        return self.per_page

    def get_context_data(self):
        context = super().get_context_data()
        context['current_page'] = self.current_page
        context['pagination'] = self.paginator
        return context
