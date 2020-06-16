from flourish import Flourish
from flourish.url import URL

import pytest


class TestFlourishUrls:
    @classmethod
    def setup_class(cls):
        with pytest.warns(None) as warnings:
            cls.flourish = Flourish('tests/source')
            assert len(warnings) == 2
            assert cls.flourish.sources.count() == 8

    def test_homepage_resolves(self):
        assert self.flourish.resolve_url('homepage') == '/'

    def test_homepage_resolves_even_with_arguments(self):
        assert self.flourish.resolve_url('homepage', tag='series') == '/'

    def test_tag_index_with_arguments_resolves(self):
        assert(self.flourish.resolve_url('tags-tag-page', tag='series') ==
               '/tags/series/')
        assert(self.flourish.resolve_url('tags-tag-page', tag='css') ==
               '/tags/css/')

    def test_tag_index_without_arguments_raises(self):
        with pytest.raises(KeyError):
            _ = self.flourish.resolve_url('tags-tag-page')

    def test_homepage_has_one_valid_filter(self):
        assert self.flourish.all_valid_filters_for_url('homepage') == [
            {}
        ]

    def test_post_detail_has_many_valid_filters(self):
        assert self.flourish.all_valid_filters_for_url('source') == [
            {'slug': 'basic-page'},
            {'slug': 'markdown-page'},
            {'slug': 'series/index'},
            {'slug': 'series/part-one'},
            {'slug': 'series/part-three'},
            {'slug': 'series/part-two'},
            {'slug': 'thing-one'},
            {'slug': 'thing-two'},
        ]

    def test_tag_index_has_many_valid_filters(self):
        assert self.flourish.all_valid_filters_for_url('tags-tag-page') == [
            {'tag': 'basic-page'},
            {'tag': 'basically'},
            {'tag': 'first'},
            {'tag': 'index'},
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
            {'tag': 'basically', 'slug': 'thing-one'},
            {'tag': 'basically', 'slug': 'thing-two'},
            {'tag': 'first', 'slug': 'thing-one'},
            {'tag': 'index', 'slug': 'series/index'},
            {'tag': 'one', 'slug': 'series/part-one'},
            {'tag': 'one', 'slug': 'thing-one'},
            {'tag': 'second', 'slug': 'thing-two'},
            {'tag': 'series', 'slug': 'series/index'},
            {'tag': 'series', 'slug': 'series/part-one'},
            {'tag': 'series', 'slug': 'series/part-three'},
            {'tag': 'series', 'slug': 'series/part-two'},
            {'tag': 'three', 'slug': 'series/part-three'},
            {'tag': 'two', 'slug': 'series/part-two'},
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
        assert self.flourish.filter(**_filters[1]).count() == 7   # 2016

    def test_month_index(self):
        _filters = self.flourish.all_valid_filters_for_url('month-index')
        assert _filters == [
            {'month': '12', 'year': '2015'},
            {'month': '02', 'year': '2016'},
            {'month': '06', 'year': '2016'},
        ]

        assert self.flourish.filter(**_filters[0]).count() == 1   # 2015/12
        assert self.flourish.filter(**_filters[1]).count() == 1   # 2016/02
        assert self.flourish.filter(**_filters[2]).count() == 6   # 2016/06

    def test_day_index(self):
        _filters = self.flourish.all_valid_filters_for_url('day-index')
        assert _filters == [
            {'day': '25', 'month': '12', 'year': '2015'},
            {'day': '29', 'month': '02', 'year': '2016'},
            {'day': '04', 'month': '06', 'year': '2016'},
            {'day': '06', 'month': '06', 'year': '2016'},
        ]

        assert self.flourish.filter(**_filters[0]).count() == 1   # 2015/12/25
        assert self.flourish.filter(**_filters[1]).count() == 1   # 2016/02/29
        assert self.flourish.filter(**_filters[2]).count() == 5   # 2016/06/04
        assert self.flourish.filter(**_filters[3]).count() == 1   # 2016/06/06

    def test_no_such_keyword_has_no_filters(self):
        assert self.flourish.all_valid_filters_for_url('no-such-keyword') == []

    def test_not_configured_has_no_filters(self):
        with pytest.raises(URL.DoesNotExist):
            _ = self.flourish.all_valid_filters_for_url('awooga')

    def test_urls_for_sources(self):
        assert [
            '/basic-page',
            '/markdown-page',
            '/thing-one',
            '/thing-two',
            '/series/',
            '/series/part-one',
            '/series/part-three',
            '/series/part-two',
        ] == [source.url for source in self.flourish.sources.all()]

    def test_lookup_url_handler(self):
        paths = (
            ('/',               ('homepage',        {})),
            ('/tags/first/',    ('tags-tag-page',   {'tag': 'first'})),
            ('/index.atom',     ('atom-feed',       {})),
            ('/thing-one',      ('source',          {'slug': 'thing-one'})),
        )
        for path, args in paths:
            matches = self.flourish.get_handler_for_path(path)
            assert matches[0] == args
        assert [] == self.flourish.get_handler_for_path('/rabble')

    def test_lookup_url_handler_wildcard(self):
        expected = [
            ('tags-tag-page',   {'tag': 'first'}),
            ('tag-post-detail', {'slug': 'thing-one', 'tag': 'first'}),
            ('tags-atom-feed',  {'tag': 'first'}),
        ]
        assert expected == self.flourish.get_handler_for_path('/tags/first/?')


class TestFlourishSourcesUrl:
    def test_category_prefixed_sources(self):
        with pytest.warns(None) as _warnings:
            _flourish = Flourish('tests/source')
            assert len(_warnings) == 2
            assert _flourish.sources.count() == 8

            _flourish.canonical_source_url(
                '/#category/#slug',
                None
            )

            assert [
                '/static/basic-page',
                '/post/markdown-page',
                '/thing/thing-one',
                '/thing/thing-two',
                '/article/series/',
                '/article/series/part-one',
                '/article/series/part-three',
                '/article/series/part-two',
            ] == [source.url for source in _flourish.sources.all()]

    def test_invalid_prefixed_sources(self):
        with pytest.warns(None) as _warnings:
            _flourish = Flourish('tests/source')
            assert len(_warnings) == 2
            assert _flourish.sources.count() == 8

            _flourish.canonical_source_url(
                '/#type/#slug',
                None
            )

            assert [
                None,
                None,
                '/post/thing-one',
                '/post/thing-two',
                '/series_index/series/',
                '/post/series/part-one',
                '/post/series/part-three',
                '/post/series/part-two',
            ] == [source.url for source in _flourish.sources.all()]
            # FIXME catch third warning

    def test_multiple_option_prefixed_sources(self):
        with pytest.warns(None) as _warnings:
            _flourish = Flourish('tests/source')
            assert len(_warnings) == 2
            assert _flourish.sources.count() == 8

            _flourish.canonical_source_url(
                '/#tag/#slug',
                None
            )

            assert [
                '/basic-page/basic-page',
                None,
                '/basically/thing-one',
                '/basically/thing-two',
                '/series/series/',
                '/series/series/part-one',
                '/three/series/part-three',
                '/series/series/part-two',
            ] == [source.url for source in _flourish.sources.all()]
            # FIXME catch third warning
