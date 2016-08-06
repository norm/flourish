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
        '/404',
        'not-found-page',
        NotFound.as_generator(),
    ),
    (
        '/tags/#tag/',
        'tags-tag-page',
        OnePageIndex.as_generator(),
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
)
