from collections.abc import Sequence
from math import ceil


# FIXME add in concertina nav
class Paginator(object):
    def __init__(self, object_list=[], per_page=10, base_path='/'):
        self.object_list = list(object_list)
        self.per_page = per_page
        self.base_path = base_path

    @property
    def count(self):
        return len(self.object_list)

    @property
    def num_pages(self):
        if self.count == 0:
            return 1
        else:
            return int(ceil(len(self.object_list) / float(self.per_page)))

    @property
    def page_range(self):
        return list(range(1, self.num_pages + 1))

    def page(self, number):
        # FIXME check this is a valid page
        start_index = (number - 1) * self.per_page
        end_index = start_index + self.per_page
        return Page(self.object_list[start_index:end_index], number, self)

    def pages(self):
        _pages = []
        for _page in self.page_range:
            _pages.append(self.page(_page))
        return _pages

    def __iter__(self):
        return iter(self.pages())


class NoPage(Exception):
    pass


class Page(Sequence):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        return self.object_list[index]

    def has_next(self):
        return self.number < self.paginator.num_pages

    def next_page_number(self):
        if self.has_next():
            return self.number + 1
        else:
            raise NoPage

    def has_previous(self):
        return self.number > 1

    def previous_page_number(self):
        if self.has_previous():
            return self.number - 1
        else:
            raise NoPage

    def has_other_pages(self):
        return self.has_next() or self.has_previous()

    def start_index(self):
        return ((self.number - 1) * self.paginator.per_page) + 1

    def end_index(self):
        return self.number * self.paginator.per_page

    @property
    def path(self):
        if self.number > 1:
            return '%s%s' % (self.paginator.base_path, 'page-%s' % self.number)
        else:
            return self.paginator.base_path
