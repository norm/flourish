from flourish.generators import (
    AtomGenerator,
    BaseGenerator,
    IndexGenerator,
    PageGenerator,
    PaginatedIndexGenerator,
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


class DatedArchive(IndexGenerator):
    order_by = ('published')


class YearIndex(DatedArchive):
    template_name = 'year.html'


class MonthIndex(DatedArchive):
    template_name = 'month.html'


class DayIndex(DatedArchive):
    template_name = 'day.html'


def global_context(self):
    return {
        'copyright_year_range': publication_range(self.flourish),
    }


GLOBAL_CONTEXT = global_context

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
        YearIndex.as_generator()
    ),
    (
        '/#year/#month/',
        'month-index',
        MonthIndex.as_generator()
    ),
    (
        '/#year/#month/#day/',
        'day-index',
        DayIndex.as_generator()
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
        '/all/',
        'all-paginated',
        FourPagePaginatedIndex.as_generator(),
    ),
    (
        '/#flooble',
        'no-such-keyword',
        NotFound.as_generator(),
    ),
)
