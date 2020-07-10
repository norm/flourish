from flourish.generators.atom import AtomGenerator
from flourish.generators.calendar import (
    CalendarYearGenerator,
    CalendarMonthGenerator,
    CalendarDayGenerator,
)
from flourish.generators.base import (
    IndexGenerator,
    PaginatedIndexGenerator,
    SourceGenerator,
    StaticGenerator,
)
from flourish.generators.sass import SassGenerator
from flourish.filters import ordinal
from flourish.helpers import publication_range


class NewestFirstIndex(IndexGenerator):
    order_by = ('-published')


class BadTemplate(NewestFirstIndex):
    template_name = 'bad.html'


class OnePageIndex(IndexGenerator):
    limit = 1


class FourPagePaginatedIndex(PaginatedIndexGenerator):
    order_by = ('published')
    per_page = 4


class NotFound(StaticGenerator):
    template_name = '404.html'


class ArchivePage(SourceGenerator):
    template_name = 'archive.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['title'] = 'Archives'
        _context['dates'] = self.flourish.publication_dates
        return _context


def global_context(self):
    return {
        'copyright_year_range': publication_range(self),
    }


GLOBAL_CONTEXT = global_context


TEMPLATE_FILTERS = {
    'ordinal': ordinal,
}





PATHS = (
    OnePageIndex(
        # something with a token comes first, as this ensures
        # that later paths still generate everything correctly
        # (ie the flourish object does not have this filter applied)
        path = '/tags/#tag/',
        name = 'tags-tag-page',
    ),
    SourceGenerator(
        path = '/tags/#tag/#slug',
        name = 'tag-post-detail',
    ),
    NewestFirstIndex(
        path = '/',
        name = 'homepage',
    ),
    BadTemplate(
        path = '/error',
        name = 'erroring-page',
    ),
    CalendarYearGenerator(
        path = '/#year/',
        name = 'year-index',
    ),
    CalendarMonthGenerator(
        path = '/#year/#month/',
        name = 'month-index',
    ),
    CalendarDayGenerator(
        path = '/#year/#month/#day/',
        name = 'day-index',
    ),
    NotFound(
        path = '/404',
        name = 'not-found-page',
        context = {
            'title': 'Not Found',
        },
    ),
    AtomGenerator(
        path = '/index.atom',
        name = 'atom-feed',
    ),
    AtomGenerator(
        path = '/tags/#tag/index.atom',
        name = 'tags-atom-feed',
    ),
    ArchivePage(
        path = '/archives',
        name = 'archives',
    ),
    FourPagePaginatedIndex(
        path = '/all/',
        name = 'all-paginated',
    ),
    SourceGenerator(
        path = '/#flooble',
        name = 'no-such-keyword',
    ),
    SassGenerator(
        path = '/css/#sass_source.css',
        name = 'sass-generated-css',
    ),
    SourceGenerator(
        path = '/#slug',
        name = 'source',
    ),
)
