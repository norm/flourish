from flourish.filters import ordinal
from flourish.generators import (
    AtomGenerator,
    BaseGenerator,
    IndexGenerator,
    PageGenerator,
    PaginatedIndexGenerator,
    SassGenerator,
    CalendarDayGenerator,
    CalendarMonthGenerator,
    CalendarYearGenerator,
)
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


class NotFound(BaseGenerator):
    template_name = '404.html'


class ArchivePage(BaseGenerator):
    template_name = 'archive.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['dates'] = self.flourish.publication_dates
        return _context


def global_context(self):
    return {
        'copyright_year_range': publication_range(self.flourish),
    }


GLOBAL_CONTEXT = global_context


TEMPLATE_FILTERS = {
    'ordinal': ordinal,
}


SOURCE_URL = (
    '/#slug',
    PageGenerator.as_generator(),
)


URLS = (
    (
        # something with a token comes first, as this ensures
        # that later URLs still generate everything correctly
        # (ie the flourish object does not have this filter applied)
        '/tags/#tag/',
        'tags-tag-page',
        OnePageIndex.as_generator(),
    ),
    (
        '/tags/#tag/#slug',
        'tag-post-detail',
        PageGenerator.as_generator()
    ),
    (
        '/',
        'homepage',
        NewestFirstIndex.as_generator(),
    ),
    (
        '/error',
        'erroring-page',
        BadTemplate.as_generator(),
    ),
    (
        '/#year/',
        'year-index',
        CalendarYearGenerator.as_generator()
    ),
    (
        '/#year/#month/',
        'month-index',
        CalendarMonthGenerator.as_generator()
    ),
    (
        '/#year/#month/#day/',
        'day-index',
        CalendarDayGenerator.as_generator()
    ),
    (
        '/404',
        'not-found-page',
        NotFound.as_generator(),
    ),
    (
        '/index.atom',
        'atom-feed',
        AtomGenerator.as_generator(),
    ),
    (
        '/tags/#tag/index.atom',
        'tags-atom-feed',
        AtomGenerator.as_generator(),
    ),
    (
        '/archives',
        'archives',
        ArchivePage.as_generator(),
    ),
    (
        '/all/',
        'all-paginated',
        FourPagePaginatedIndex.as_generator(),
    ),
    (
        '/#flooble',
        'no-such-keyword',
        NotFound.as_generator(),
    ),
    (
        '/css/#slug.css',
        'sass-generated-css',
        SassGenerator.as_generator(),
    ),
)
