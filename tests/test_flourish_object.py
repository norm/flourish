from datetime import datetime

import pytest

from flourish import Flourish, TomlSourceFile


class TestFlourishNoArgs:
    def test_without_source_raises(self):
        with pytest.raises(AttributeError):
            Flourish()


class TestFlourish:
    @classmethod
    def setup_class(cls):
        cls.flourish = Flourish('tests/source')

    def test_get_all_sources(self):
        sources = self.flourish.sources.all()
        assert type(sources) == Flourish
        assert len(sources) == 6
        # os.walk order, root dir before subdirs, alphabetical order
        assert [
                'basic-page',
                'thing-one',
                'thing-two',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_get_one_source_by_slug(self):
        source = self.flourish.sources.get('basic-page')
        assert type(source) == TomlSourceFile
        assert source.slug == 'basic-page'

        source = self.flourish.sources.get('series/part-two')
        assert type(source) == TomlSourceFile
        assert source.slug == 'series/part-two'

    def test_get_missing_source_raises(self):
        with pytest.raises(TomlSourceFile.DoesNotExist):
            self.flourish.sources.get('nope')

    def test_get_by_index(self):
        source = self.flourish.sources.all()[0]
        assert type(source) == TomlSourceFile

    def test_get_by_negative_index_raises(self):
        with pytest.raises(ValueError):
            self.flourish.sources.all()[-1]

    def test_get_by_bad_index_raises(self):
        with pytest.raises(IndexError):
            self.flourish.sources.all()[100]

    def test_get_sources_by_slice(self):
        sources = self.flourish.sources.all()[0:2]
        assert type(sources) == Flourish
        assert len(sources) == 2
        assert [
                'basic-page',
                'thing-one',
            ] == [source.slug for source in sources]

    def test_get_sources_by_negative_slice_raises(self):
        with pytest.raises(ValueError):
            self.flourish.sources.all()[-2:2]

    def test_get_sources_with_ordering(self):
        sources = self.flourish.sources.all().order_by('published')
        assert type(sources) == Flourish
        assert len(sources) == 6
        assert [
                'basic-page',
                'series/part-one',
                'series/part-two',
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in sources]

        sources = self.flourish.sources.all().order_by('-published')
        assert type(sources) == Flourish
        assert len(sources) == 6
        # thing-one and thing-two swap places (aren't reversed) because they
        # share a published timestamp, so come out in alphabetical order
        assert [
                'series/part-three',
                'thing-one',
                'thing-two',
                'series/part-two',
                'series/part-one',
                'basic-page',
            ] == [source.slug for source in sources]

        sources = self.flourish.sources.all().order_by('title')
        assert type(sources) == Flourish
        assert len(sources) == 6
        assert [
                'basic-page',
                'series/part-one',
                'series/part-three',
                'series/part-two',
                'thing-two',
                'thing-one',
            ] == [source.slug for source in sources]

    def test_order_by_key_not_in_all_sources_issues_warning(self):
        with pytest.warns(None) as warnings:
            sources = self.flourish.sources.all().order_by('-updated')
            assert type(sources) == Flourish
            assert len(sources) == 6
            # os.walk order, root dir first, alphabetical order
            assert [
                    'basic-page',
                    'thing-one',
                    'thing-two',
                    'series/part-one',
                    'series/part-three',
                    'series/part-two',
                ] == [source.slug for source in sources]
            # twice, once for `len(sources)`, once for `for source in sources`
            assert len(warnings) == 2
            assert (
                str(warnings[0].message) ==
                'sorting sources by "-updated" failed: '
                'not all sources have that attribute'
            )

    def test_order_by_multiple_keys(self):
        sources = self.flourish.sources.all().order_by('title', '-published')
        assert type(sources) == Flourish
        assert len(sources) == 6
        # thing-one and thing-two come out in reverse order compared to
        # plain order_by('-published') because they share a published
        # timestamp, but the extra title argument sorted them differently
        # from the slug-alphabetical sort order
        assert [
                'series/part-three',
                'thing-two',
                'thing-one',
                'series/part-two',
                'series/part-one',
                'basic-page',
            ] == [source.slug for source in sources]

    def test_filter_equal_to(self):
        on = datetime(2016, 06, 04, 12, 30, 0)
        sources = self.flourish.sources.filter(published=on)
        assert type(sources) == Flourish
        assert len(sources) == 2
        assert [
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

    def test_filter_equal_to_where_sources_have_missing_keys(self):
        # not all sources have `series` declared, this should not raise
        sources = self.flourish.sources.filter(series='series-in-three-parts')
        assert type(sources) == Flourish
        assert len(sources) == 3
        assert [
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_less_than(self):
        on = datetime(2016, 06, 04, 12, 30, 0)
        sources = self.flourish.sources.filter(published__lt=on)
        assert type(sources) == Flourish
        assert len(sources) == 3
        assert [
                'basic-page',
                'series/part-one',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_less_than_or_equal_to(self):
        on = datetime(2016, 06, 04, 12, 30, 0)
        sources = self.flourish.sources.filter(published__lte=on)
        assert type(sources) == Flourish
        assert len(sources) == 5
        assert [
                'basic-page',
                'thing-one',
                'thing-two',
                'series/part-one',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_greater_than(self):
        on = datetime(2016, 06, 04, 12, 30, 0)
        sources = self.flourish.sources.filter(published__gt=on)
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_filter_greater_than_or_equal_to(self):
        on = datetime(2016, 06, 04, 12, 30, 0)
        sources = self.flourish.sources.filter(published__gte=on)
        assert type(sources) == Flourish
        assert len(sources) == 3
        assert [
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_filter_contains(self):
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should both be matched
        sources = self.flourish.sources.filter(tag__contains='basic')
        assert type(sources) == Flourish
        assert len(sources) == 3
        assert [
                'basic-page',
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

    def test_filter_contains_invalid_value(self):
        sources = self.flourish.sources.filter(published__contains='two')
        assert type(sources) == Flourish
        assert len(sources) == 0

    def test_filter_contains_on_string(self):
        sources = self.flourish.sources.filter(title__contains='the')
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'thing-one',
            ] == [source.slug for source in sources]

    def test_filter_in_list(self):
        categories = ['article', 'thing']
        sources = self.flourish.sources.filter(category__in=categories)
        assert type(sources) == Flourish
        assert len(sources) == 5
        assert [
                'thing-one',
                'thing-two',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_set(self):
        sources = self.flourish.sources.filter(type__set='')
        assert type(sources) == Flourish
        assert len(sources) == 5
        assert [
                'thing-one',
                'thing-two',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_unset(self):
        sources = self.flourish.sources.filter(type__unset='')
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'basic-page',
            ] == [source.slug for source in sources]

    def test_filter_inside_or_equal(self):
        # in contrast to test_filter_contains above, 
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should not be matched
        sources = self.flourish.sources.filter(tag='basic')
        assert type(sources) == Flourish
        assert len(sources) == 0

        # ... but 'basically' should
        sources = self.flourish.sources.filter(tag='basically')
        assert type(sources) == Flourish
        assert len(sources) == 2
        assert [
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

        # ... as should 'basic-page'
        sources = self.flourish.sources.filter(tag='basic-page')
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'basic-page',
            ] == [source.slug for source in sources]

    def test_filter_multiple_arguments(self):
        # only two sources have the tag 'two'; three of the six sources were
        # published before 12:15, three published after 12:15; filtering
        # against both of these should only find one post in each subgroup
        on = datetime(2016, 06, 04, 12, 15, 0)
        sources = self.flourish.sources.filter(
            tag__contains='two', published__gt=on)
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'thing-two',
            ] == [source.slug for source in sources]

        sources = self.flourish.sources.filter(
            tag__contains='two', published__lt=on)
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'series/part-two',
            ] == [source.slug for source in sources]

        # can "stack" .filter() as well as use multiple arguments to it
        two_sources = self.flourish.sources.filter(tag__contains='two')
        sources = two_sources.filter(published__gt=on)
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'thing-two',
            ] == [source.slug for source in sources]

        sources = two_sources.filter(published__lt=on)
        assert type(sources) == Flourish
        assert len(sources) == 1
        assert [
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_after_order_works(self):
        sources = self.flourish.sources.filter(tag__contains='two')
        assert type(sources) == Flourish
        assert len(sources) == 2
        assert [
                'thing-two',
                'series/part-two',
            ] == [source.slug for source in sources]

        sources = sources.order_by('published')
        assert [
                'series/part-two',
                'thing-two',
            ] == [source.slug for source in sources]

    def test_order_after_filter_works(self):
        sources = self.flourish.sources.order_by('published')
        assert type(sources) == Flourish
        assert len(sources) == 6

        sources = sources.filter(tag__contains='one')
        assert [
                'series/part-one',
                'thing-one',
            ] == [source.slug for source in sources]

    def test_order_after_filter_does_not_warn_on_absent_keys(self):
        with pytest.warns(None) as warnings:
            sources = self.flourish.sources.order_by('type')
            assert type(sources) == Flourish
            assert len(sources) == 6
            assert len(warnings) == 1
            assert (
                str(warnings[0].message) ==
                'sorting sources by "type" failed: '
                'not all sources have that attribute'
            )

        with pytest.warns(None) as warnings:
            sources = self.flourish.sources.filter(type='post')
            assert len(sources) == 5
            sources = sources.order_by('type', 'published')
            assert type(sources) == Flourish
            assert len(sources) == 5
            assert len(warnings) == 0
            assert [
                    'series/part-one',
                    'series/part-two',
                    'thing-one',
                    'thing-two',
                    'series/part-three',
                ] == [source.slug for source in sources]
