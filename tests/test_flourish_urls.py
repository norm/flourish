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
            cls.flourish.add_url(
                '/#slug',
                'post-detail',
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
        assert self.flourish.all_valid_filters_for_url('post-detail') == [
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
