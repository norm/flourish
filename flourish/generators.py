from datetime import datetime
import os

from pyatom import AtomFeed


class MissingValue(Exception):
    pass


class PageContextMixin(object):
    def get_context_data(self):
        _context = super(PageContextMixin, self).get_context_data()
        _context['page'] = self.source_objects[0]
        _context.update(self.source_objects[0]._config)
        return _context


class PageIndexContextMixin(object):
    def get_context_data(self):
        _context = super(PageIndexContextMixin, self).get_context_data()
        _context['pages'] = self.source_objects
        return _context


class BaseGenerator(object):
    order_by = None
    sources_filter = None
    template_name = None

    @classmethod
    def as_generator(cls):
        def generator(flourish, url):
            self = cls(flourish, url)
            return self.generate()

        return generator

    def __init__(self, flourish, url):
        self.flourish = flourish
        self.url = url
        self.current_url = None

    def generate(self):
        for _tokens in self.get_url_tokens():
            self.get_current_url(_tokens)
            self.get_objects(_tokens)
            self.output_to_file()

    def get_url_tokens(self):
        self.valid_filters = \
            self.flourish.all_valid_filters_for_url(self.url.name)
        return self.valid_filters

    def get_current_url(self, tokens):
        self.current_url = self.url.resolve(**tokens)
        return self.current_url

    def get_objects(self, tokens):
        _filtered = self.get_filtered_sources().filter(**tokens)
        _ordering = self.get_order_by()
        if _ordering is not None:
            _filtered = _filtered.order_by(self.order_by)

        self.source_objects = _filtered
        return self.source_objects

    def get_filtered_sources(self):
        _sources = self.flourish.sources
        if self.sources_filter is not None:
            _sources = self.flourish.filter(**self.sources_filter)
        return _sources

    def get_order_by(self):
        return self.order_by

    def output_to_file(self):
        _filename = self.get_output_filename()
        _rendered = self.render_output()
        _directory = os.path.dirname(_filename)
        if not os.path.isdir(_directory):
            os.makedirs(_directory)
        with open(_filename, 'w') as _output:
            _output.write(_rendered)

    def get_output_filename(self):
        _destination = '%s%s' % (self.flourish.output_dir, self.current_url)
        if _destination.endswith('/'):
            _destination = _destination + 'index.html'
        if not _destination.endswith(('.html', '.atom')):
            _destination = _destination + '.html'
        return _destination

    def render_output(self):
        _context = self.get_context_data()
        _template = self.get_template()
        return self.render_template(_template, _context)

    def get_context_data(self):
        _context = {}
        _context['objects'] = self.source_objects
        _context['site'] = self.flourish.site_config
        return _context

    def get_template(self):
        _name = self.get_template_name()
        if _name is None:
            raise MissingValue
        return self.flourish.jinja.get_template(_name)

    def get_template_name(self):
        return self.template_name

    def render_template(self, template, context_data):
        return template.render(context_data).encode('UTF-8')


class PageGenerator(PageContextMixin, BaseGenerator):
    template_name = 'page.html'

    def get_template_name(self):
        if 'template' in self.source_objects[0]:
            return self.source_objects[0]['template']
        if 'type' in self.source_objects[0]:
            return '%s.html' % self.source_objects[0]['type']
        return super(PageGenerator, self).get_template_name()


class IndexGenerator(PageIndexContextMixin, BaseGenerator):
    template_name = 'index.html'


class AtomGenerator(BaseGenerator):
    order_by = ('-published')

    def get_objects(self, tokens):
        """
        Only consider objects that have the key "published" with a
        datetime value that is in the past.
        """
        _now = datetime.now()
        _sources = self.get_filtered_sources()
        _already_published = _sources.filter(published__lt=_now)
        _filtered = _already_published.filter(**tokens)
        _ordered = _filtered.order_by(self.order_by)
        self.source_objects = _ordered
        return self.source_objects

    def render_output(self):
        _feed_global = {
            'author': self.flourish.site_config['author'],
            'title': self.flourish.site_config['title'],
            'url': self.flourish.site_config['base_url'],
            'feed_url': '%s%s' % (
                self.flourish.site_config['base_url'],
                self.current_url,
            ),
        }
        _feed = AtomFeed(**_feed_global)

        for _object in self.source_objects:
            entry = {
                'title': _object.title,
                'content': _object.body,
                'content_type': 'html',
                'url': _object.absolute_url,
                'published': _object.published,
                'updated': _object.published,
                'author': self.flourish.site_config['author'],
            }
            if 'author' in _object:
                entry['author'] = _object.author
            if 'updated' in _object:
                entry['updated'] = _object.updated
            _feed.add(**entry)

        return _feed.to_string()
