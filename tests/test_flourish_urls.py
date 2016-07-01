from flourish import Flourish

import pytest


class TestFlourishUrls:
    @classmethod
    def setup_class(cls):
        with pytest.warns(None) as warnings:
            cls.flourish = Flourish('tests/source')
            assert len(warnings) == 2
            assert cls.flourish.sources.count() == 7

            cls.flourish.add_url(
                '/',
                'homepage',
                None
            )
            cls.flourish.canonical_source_url(
                '/#slug',
                None
            )
            cls.flourish.add_url(
                '/tags/#tag/',
                'tag-index',
                None
            )
            cls.flourish.add_url(
                '/tags/#tag/#slug',
                'tag-post-detail',
                None
            )
            cls.flourish.add_url(
                '/#year/',
                'year-index',
                None
            )
            cls.flourish.add_url(
                '/#year/#month/',
                'month-index',
                None
            )
            cls.flourish.add_url(
                '/#year/#month/#day',
                'day-index',
                None
            )
            cls.flourish.add_url(
                '/#flooble',
                'no-such-keyword',
                None
            )

    def test_homepage_resolves(self):
        assert self.flourish.resolve_url('homepage') == '/'

    def test_homepage_resolves_even_with_arguments(self):
        assert self.flourish.resolve_url('homepage', tag='series') == '/'

    def test_tag_index_with_arguments_resolves(self):
        assert(self.flourish.resolve_url('tag-index', tag='series') ==
               '/tags/series/')
        assert(self.flourish.resolve_url('tag-index', tag='css') ==
               '/tags/css/')

    def test_tag_index_without_arguments_raises(self):
        with pytest.raises(KeyError):
            self.flourish.resolve_url('tag-index')

    def test_homepage_has_one_valid_filter(self):
        assert self.flourish.all_valid_filters_for_url('homepage') == [
            {}
        ]

    def test_post_detail_has_many_valid_filters(self):
        assert self.flourish.all_valid_filters_for_url('source') == [
            {'slug': 'basic-page'},
            {'slug': 'markdown-page'},
            {'slug': 'series/part-one'},
            {'slug': 'series/part-three'},
            {'slug': 'series/part-two'},
            {'slug': 'thing-one'},
            {'slug': 'thing-two'},
        ]

    def test_tag_index_has_many_valid_filters(self):
        assert self.flourish.all_valid_filters_for_url('tag-index') == [
            {'tag': 'basic-page'},
            {'tag': 'basically'},
            {'tag': 'first'},
            {'tag': 'one'},
            {'tag': 'second'},
            {'tag': 'series'},
            {'tag': 'three'},
            {'tag': 'two'},
        ]

    def test_tag_post_detail_resolves_to_many_with_only_one_source_each(self):
        _filters = self.flourish.all_valid_filters_for_url('tag-post-detail')
        assert _filters == [
            {'tag': 'basic-page', 'slug': 'basic-page'},
            {'tag': 'one', 'slug': 'series/part-one'},
            {'tag': 'series', 'slug': 'series/part-one'},
            {'tag': 'series', 'slug': 'series/part-three'},
            {'tag': 'three', 'slug': 'series/part-three'},
            {'tag': 'series', 'slug': 'series/part-two'},
            {'tag': 'two', 'slug': 'series/part-two'},
            {'tag': 'basically', 'slug': 'thing-one'},
            {'tag': 'first', 'slug': 'thing-one'},
            {'tag': 'one', 'slug': 'thing-one'},
            {'tag': 'basically', 'slug': 'thing-two'},
            {'tag': 'second', 'slug': 'thing-two'},
            {'tag': 'two', 'slug': 'thing-two'},
        ]

        # as the filters include `slug` (which is unique),
        # each should only match one source
        for _filter in _filters:
            assert self.flourish.sources.filter(**_filter).count() == 1

    def test_year_index(self):
        _filters = self.flourish.all_valid_filters_for_url('year-index')
        assert _filters == [
            {'year': '2015'},
            {'year': '2016'},
        ]

        assert self.flourish.filter(**_filters[0]).count() == 1   # 2015
        assert self.flourish.filter(**_filters[1]).count() == 6   # 2016

    def test_month_index(self):
        _filters = self.flourish.all_valid_filters_for_url('month-index')
        assert _filters == [
            {'month': '02', 'year': '2016'},
            {'month': '06', 'year': '2016'},
            {'month': '12', 'year': '2015'},
        ]

        assert self.flourish.filter(**_filters[0]).count() == 1   # 2016/02
        assert self.flourish.filter(**_filters[1]).count() == 5   # 2016/06
        assert self.flourish.filter(**_filters[2]).count() == 1   # 2015/12

    def test_day_index(self):
        _filters = self.flourish.all_valid_filters_for_url('day-index')
        assert _filters == [
            {'day': '04', 'month': '06', 'year': '2016'},
            {'day': '06', 'month': '06', 'year': '2016'},
            {'day': '25', 'month': '12', 'year': '2015'},
            {'day': '29', 'month': '02', 'year': '2016'},
        ]

        assert self.flourish.filter(**_filters[0]).count() == 4   # 2016/06/04
        assert self.flourish.filter(**_filters[1]).count() == 1   # 2016/06/06
        assert self.flourish.filter(**_filters[1]).count() == 1   # 2015/12/25
        assert self.flourish.filter(**_filters[2]).count() == 1   # 2016/02/29

    def test_no_such_keyword_has_no_filters(self):
        assert self.flourish.all_valid_filters_for_url('no-such-keyword') == []

    def test_urls_for_sources(self):
        assert [
            '/basic-page',
            '/markdown-page',
            '/thing-one',
            '/thing-two',
            '/series/part-one',
            '/series/part-three',
            '/series/part-two',
        ] == [source.url for source in self.flourish.sources.all()]


class TestFlourishSourcesUrl:
    def test_category_prefixed_sources(self):
        with pytest.warns(None) as _warnings:
            _flourish = Flourish('tests/source')
            assert len(_warnings) == 2
            assert _flourish.sources.count() == 7

            _flourish.canonical_source_url(
                '/#category/#slug',
                None
            )

            assert [
                '/static/basic-page',
                '/post/markdown-page',
                '/thing/thing-one',
                '/thing/thing-two',
                '/article/series/part-one',
                '/article/series/part-three',
                '/article/series/part-two',
            ] == [source.url for source in _flourish.sources.all()]

    def test_invalid_prefixed_sources(self):
        with pytest.warns(None) as _warnings:
            _flourish = Flourish('tests/source')
            assert len(_warnings) == 2
            assert _flourish.sources.count() == 7

            _flourish.canonical_source_url(
                '/#type/#slug',
                None
            )

            assert [
                None,
                None,
                '/post/thing-one',
                '/post/thing-two',
                '/post/series/part-one',
                '/post/series/part-three',
                '/post/series/part-two',
            ] == [source.url for source in _flourish.sources.all()]
            # FIXME catch third warning

    def test_multiple_option_prefixed_sources(self):
        with pytest.warns(None) as _warnings:
            _flourish = Flourish('tests/source')
            assert len(_warnings) == 2
            assert _flourish.sources.count() == 7

            _flourish.canonical_source_url(
                '/#tag/#slug',
                None
            )

            assert [
                '/basic-page/basic-page',
                None,
                '/basically/thing-one',
                '/basically/thing-two',
                '/series/series/part-one',
                '/three/series/part-three',
                '/series/series/part-two',
            ] == [source.url for source in _flourish.sources.all()]
            # FIXME catch third warning
