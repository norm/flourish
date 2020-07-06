from datetime import datetime, timezone, date
import os

from feedgen.feed import FeedGenerator
import sass

from .paginator import Paginator


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
        _context['tokens'] = self._tokens
        return _context


class BaseGenerator(object):
    order_by = None
    sources_exclude = None
    sources_filter = None
    template_name = None
    limit = None
    file_extension = '.html'

    @classmethod
    def as_generator(cls):
        def generator(
            flourish,
            url,
            global_context=None,
            report=False,
            tokens=None,
        ):
            self = cls(flourish, url, global_context, report)
            return self.generate(tokens)

        return generator

    def __init__(self, flourish, url, global_context, report):
        self.flourish = flourish
        self.url = url
        self.global_context = global_context
        self.current_url = None
        self.report = report

    def generate_path(self, _tokens):
        self.get_current_url(_tokens)
        self.get_objects(_tokens)
        self.output_to_file()

    def generate(self, _tokens=None):
        if not _tokens:
            _tokens = self.get_url_tokens()
        for _t in _tokens:
            self._tokens = _t
            self.generate_path(_t)

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

        if self.limit is not None:
            self.source_objects = _filtered[0:self.limit]
        else:
            self.source_objects = _filtered
        return self.source_objects

    def get_filtered_sources(self):
        _sources = self.flourish.sources
        if self.sources_filter is not None:
            _sources = self.flourish.filter(**self.sources_filter)
        if self.sources_exclude is not None:
            _sources = self.flourish.exclude(**self.sources_exclude)
        return _sources

    def get_order_by(self):
        return self.order_by

    def output_to_file(self):
        _filename = self.get_output_filename()
        if self.report:
            print('->', _filename)

        _rendered = self.render_output()
        _directory = os.path.dirname(_filename)
        if not os.path.isdir(_directory):
            os.makedirs(_directory)
        with open(_filename, 'w', encoding='utf8') as _output:
            _output.write(_rendered)

    def get_output_filename(self):
        _destination = '%s%s' % (self.flourish.output_dir, self.current_url)
        if _destination.endswith('/'):
            _destination = _destination + 'index.html'
        if not _destination.endswith(self.file_extension):
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
        _context['current_url'] = self.current_url
        if self.global_context is not None:
            _context['global'] = self.global_context(self)
        return _context

    def get_template(self):
        _name = self.get_template_name()
        if _name is None:
            raise MissingValue
        return self.flourish.jinja.get_template(_name)

    def get_template_name(self):
        return self.template_name

    def render_template(self, template, context_data):
        return template.render(context_data)


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


class PaginatedIndexGenerator(IndexGenerator):
    per_page = 10

    def generate_path(self, _tokens):
        _base_url = self.get_current_url(_tokens)
        _paginator = self.get_paginated_objects(_tokens, _base_url)
        for _page in _paginator:
            self.current_url = _page.url
            self.source_objects = _page.object_list
            self.current_page = _page
            self.output_to_file()

    def get_paginated_objects(self, tokens, base_url):
        _objects = self.get_objects(tokens)
        _per_page = self.get_per_page()
        self.paginator = Paginator(_objects, _per_page, base_url)
        return self.paginator

    def get_per_page(self):
        return self.per_page

    def get_context_data(self):
        _context = super(PaginatedIndexGenerator, self).get_context_data()
        _context['current_page'] = self.current_page
        _context['pagination'] = self.paginator
        return _context


class AtomGenerator(BaseGenerator):
    order_by = ('-published')
    file_extension = '.atom'

    def get_objects(self, tokens):
        """
        Only consider objects that have the key "published" with a
        datetime value that is in the past.
        """
        _now = datetime.now().replace(tzinfo=timezone.utc)
        _sources = self.get_filtered_sources()
        _already_published = _sources.filter(published__lt=_now)
        _filtered = _already_published.filter(**tokens)
        _ordered = _filtered.order_by(self.order_by)

        if self.limit is not None:
            self.source_objects = _ordered[0:self.limit]
        else:
            self.source_objects = _ordered

        return self.source_objects

    def render_output(self):
        feed = FeedGenerator()
        feed.author({'name': self.flourish.site_config['author']})
        feed.title(self.flourish.site_config['title'])
        # feed.link(self.flourish.site_config['base_url'])
        feed.id('%s%s' % (
            self.flourish.site_config['base_url'],
            self.current_url,
        ))
        feed.link(href='%s%s' % (
                self.flourish.site_config['base_url'],
                self.current_url,
            ), rel='self')
        feed.link(href=self.flourish.site_config['base_url'], rel='alternate')

        last_updated = self.source_objects[0].published

        for _object in self.source_objects:
            entry = feed.add_entry(order='append')
            entry.title(_object.title)
            entry.id(_object.absolute_url)
            entry.link(href=_object.absolute_url, rel='alternate')
            entry.published(_object.published)
            entry.content(content=_object.body, type='html')

            if 'author' in _object:
                entry.author({'name': _object.author})
            else:
                entry.author({'name': self.flourish.site_config['author']})

            if 'updated' in _object:
                entry.updated(_object.updated)
                if _object.updated > last_updated:
                    last_updated = _object.updated
            else:
                entry.updated(_object.published)

        feed.updated(last_updated)

        return feed.atom_str(pretty=True)

    # FIXME refactor
    def output_to_file(self):
        _filename = self.get_output_filename()
        if self.report:
            print('->', _filename)

        _rendered = self.render_output()
        _directory = os.path.dirname(_filename)
        if not os.path.isdir(_directory):
            os.makedirs(_directory)
        with open(_filename, 'wb') as _output:
            _output.write(_rendered)


class SassGenerator(BaseGenerator):
    output_dir = 'css'
    output_style = 'expanded'
    file_extension = '.css'

    def get_url_tokens(self):
        tokens = []
        for root, dirs, files in os.walk(self.flourish.sass_dir):
            root = root[len(self.flourish.sass_dir):]
            for file in files:
                base, ext = os.path.splitext(file)
                if not base.startswith('_') and ext == '.scss':
                    tokens.append(os.path.join(root, base))
        return tokens

    def get_current_url(self, tokens):
        self.current_url = os.path.join(
            '/',
            self.get_output_dir(),
            '%s.css' % tokens
        )
        return self.current_url

    def get_output_dir(self):
        return self.output_dir

    def get_objects(self, tokens):
        # there are no Source objects
        pass

    def render_output(self):
        source = os.path.join(
            self.flourish.sass_dir,
            '%s.scss' % self._tokens,
        )
        return sass.compile(
            filename=source,
            output_style=self.output_style,
        )


class CalendarGenerator(IndexGenerator):
    order_by = 'published'


class CalendarDayGenerator(CalendarGenerator):
    template_name = 'calendar_day.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['day'] = date(
            day=int(self._tokens['day']),
            month=int(self._tokens['month']),
            year=int(self._tokens['year']),
        )
        return _context


class CalendarMonthGenerator(CalendarGenerator):
    template_name = 'calendar_month.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['month'] = date(
            day=int(1),
            month=int(self._tokens['month']),
            year=int(self._tokens['year']),
        )
        dates = self.source_objects.publication_dates
        _context['publication_dates'] = dates[0]['months'][0]['days']
        return _context


class CalendarYearGenerator(CalendarGenerator):
    template_name = 'calendar_year.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['year'] = date(
            day=1,
            month=1,
            year=int(self._tokens['year']),
        )
        dates = self.source_objects.publication_dates
        _context['publication_dates'] = dates[0]['months']
        return _context
