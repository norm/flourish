import pytest

from flourish.paginator import Paginator, NoPage


class TestPaginator:
    def test_paginator_no_objects_produces_a_page_anyway(self):
        paginator = Paginator(object_list=[], per_page=10)
        assert paginator.count == 0
        assert paginator.num_pages == 1
        assert paginator.page_range == [1, ]

    def test_paginator_lte_per_page_produces_a_page(self):
        paginator = Paginator(object_list=[1, 2, 3], per_page=10)
        assert paginator.count == 3
        assert paginator.num_pages == 1
        assert paginator.page_range == [1, ]

    def test_paginator_gt_per_page_produces_more_than_one_page(self):
        paginator = Paginator(object_list=range(1, 15), per_page=10)
        assert paginator.count == 14
        assert paginator.num_pages == 2
        assert paginator.page_range == [1, 2, ]

    def test_short_paginator_pages(self):
        paginator = Paginator(object_list=range(1, 15), per_page=3)
        assert paginator.count == 14
        assert paginator.num_pages == 5
        assert paginator.page_range == [1, 2, 3, 4, 5]


class TestPage:
    @classmethod
    def setup_class(cls):
        cls.paginator = Paginator(object_list=range(1, 15), per_page=10)

    def test_no_other_pages(self):
        short_paginator = Paginator(object_list=[1, 2], per_page=10)
        page = short_paginator.page(1)
        assert page.start_index() == 1
        assert page.end_index() == 10
        assert page.has_previous() is False
        assert page.has_next() is False
        assert page.has_other_pages() is False

    def test_page_one_has_no_previous(self):
        page = self.paginator.page(1)
        assert page.start_index() == 1
        assert page.end_index() == 10
        assert page.has_previous() is False
        assert page.has_other_pages() is True
        with pytest.raises(NoPage):
            page.previous_page_number()

    def test_page_one_has_next(self):
        page = self.paginator.page(1)
        assert page.start_index() == 1
        assert page.end_index() == 10
        assert page.has_next() is True
        assert page.has_other_pages() is True
        assert page.next_page_number() == 2

    def test_page_two_has_previous(self):
        page = self.paginator.page(2)
        assert page.start_index() == 11
        assert page.end_index() == 20
        assert page.has_previous() is True
        assert page.has_other_pages() is True
        assert page.previous_page_number() == 1

    def test_page_two_has_no_next(self):
        page = self.paginator.page(2)
        assert page.start_index() == 11
        assert page.end_index() == 20
        assert page.has_next() is False
        assert page.has_other_pages() is True
        with pytest.raises(NoPage):
            page.next_page_number()

    def test_short_pages(self):
        paginator = Paginator(object_list=range(1, 15), per_page=3)
        page = paginator.page(2)
        assert page.start_index() == 4
        assert page.end_index() == 6
        assert page.has_next() is True
        assert page.has_other_pages() is True
        assert page.next_page_number() == 3
        assert page.object_list == [4, 5, 6]
