from datetime import date, datetime, timezone

import pytest

from flourish import Flourish, JsonSourceFile, SourceList, TomlSourceFile


class TestFlourishNoArgs:
    def test_without_source_raises(self):
        with pytest.raises(AttributeError):
            Flourish()


class TestFlourishSiteConfigRequirements:
    def test_empty_site_config_is_error(self):
        with pytest.raises(Flourish.MissingKey):
            Flourish('tests/invalid_siteconfig')


class TestFlourish:
    @classmethod
    def setup_class(cls):
        with pytest.warns(None) as warnings:
            cls.flourish = Flourish('tests/source')
            assert len(warnings) == 2
            assert cls.flourish.sources.count() == 9

    def test_get_all_sources(self):
        sources = self.flourish.sources.all()
        assert type(sources) == SourceList
        assert len(sources) == 9
        # os.walk order, root dir before subdirs, alphabetical order
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_get_one_source_by_slug(self):
        source = self.flourish.get('basic-page')
        assert type(source) == TomlSourceFile
        assert source.slug == 'basic-page'

        source = self.flourish.get('series/part-two')
        assert type(source) == TomlSourceFile
        assert source.slug == 'series/part-two'

    def test_get_missing_source_raises(self):
        with pytest.raises(TomlSourceFile.DoesNotExist):
            self.flourish.get('nope')

        with pytest.raises(TomlSourceFile.DoesNotExist):
            self.flourish.get('invalid-name.things')

    def test_get_by_index(self):
        source = self.flourish.sources.all()[3]
        assert type(source) == JsonSourceFile
        assert source.slug == 'thing-one'

    def test_get_by_negative_index(self):
        source = self.flourish.sources.all()[-6]
        assert type(source) == JsonSourceFile
        assert source.slug == 'thing-one'

    def test_get_by_bad_index_raises(self):
        with pytest.raises(IndexError):
            self.flourish.sources.all()[100]

    def test_get_sources_by_slice(self):
        sources = self.flourish.sources.all()[0:2]
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'basic-page',
                'markdown-page',
            ] == [source.slug for source in sources]

    def test_get_filtered_sources_by_slice(self):
        sources = self.flourish.sources.filter(series__set='')
        assert type(sources) == SourceList
        assert len(sources) == 4
        assert [
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

        assert [
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources[2:]]

    def test_get_sources_by_negative_values(self):
        sources = self.flourish.sources.all()[-3:-1]
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'series/part-one',
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_get_sources_by_negative_stop(self):
        sources = self.flourish.sources.all()[:-4]
        assert type(sources) == SourceList
        assert len(sources) == 5
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

    def test_get_sources_with_ordering(self):
        sources = self.flourish.sources.filter(published__set='')
        # just those with a published key
        published = sources.order_by('published')
        assert type(published) == SourceList
        assert len(published) == 8
        assert [
                'basic-page',
                'markdown-page',
                'series/index',
                'series/part-one',
                'series/part-two',
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in published]

        rev_published = sources.order_by('-published')
        assert type(rev_published) == SourceList
        assert len(rev_published) == 8
        # thing-one and thing-two swap places (aren't reversed) because they
        # share a published timestamp, so come out in alphabetical order
        assert [
                'series/part-three',
                'thing-one',
                'thing-two',
                'series/part-two',
                'series/part-one',
                'series/index',
                'markdown-page',
                'basic-page',
            ] == [source.slug for source in rev_published]

        titled = self.flourish.sources.all().order_by('title')
        assert type(titled) == SourceList
        assert len(titled) == 9
        assert [
                'series/index',
                'basic-page',
                'nothing',
                'series/part-one',
                'series/part-three',
                'series/part-two',
                'markdown-page',
                'thing-two',
                'thing-one',
            ] == [source.slug for source in titled]

    def test_get_sources_with_ordering_and_slice(self):
        sources = self.flourish.sources.filter(published__set='')
        # just those with a published key
        published = sources.order_by('published')
        assert type(published) == SourceList
        assert len(published) == 8
        assert [
                'basic-page',
                'markdown-page',
                'series/index',
                'series/part-one',
                'series/part-two',
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in published]

        assert [
                'basic-page',
                'markdown-page',
                'series/index',
        ] == [source.slug for source in published[0:3]]

    def test_order_by_key_not_in_all_sources_issues_warning(self):
        with pytest.warns(None) as warnings:
            sources = self.flourish.sources.all().order_by('-updated')
            assert type(sources) == SourceList
            assert len(sources) == 9
            # os.walk order, root dir first, alphabetical order
            assert [
                    'basic-page',
                    'markdown-page',
                    'nothing',
                    'thing-one',
                    'thing-two',
                    'series/index',
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
        sources = self.flourish.sources.filter(published__set='')
        sorted_sources = sources.order_by('title', '-published')
        assert type(sorted_sources) == SourceList
        assert len(sorted_sources) == 8
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
                'series/index',
                'markdown-page',
                'basic-page',
            ] == [source.slug for source in sorted_sources]

    def test_filter_equal_to(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.filter(published=on)
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

    def test_exclude_equal_to(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.exclude(published=on)
        assert type(sources) == SourceList
        assert len(sources) == 7
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_equal_to_where_sources_have_missing_keys(self):
        # not all sources have `series` declared, this should not raise
        sources = self.flourish.sources.filter(series='series-in-three-parts')
        assert type(sources) == SourceList
        assert len(sources) == 4
        assert [
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_less_than(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.filter(published__lt=on)
        assert type(sources) == SourceList
        assert len(sources) == 5
        assert [
                'basic-page',
                'markdown-page',
                'series/index',
                'series/part-one',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_less_than(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.exclude(published__lt=on)
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_filter_less_than_or_equal_to(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.filter(published__lte=on)
        assert type(sources) == SourceList
        assert len(sources) == 7
        assert [
                'basic-page',
                'markdown-page',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_less_than_or_equal_to(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.exclude(published__lte=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_filter_greater_than(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.filter(published__gt=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_exclude_greater_than(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.exclude(published__gt=on)
        assert type(sources) == SourceList
        assert len(sources) == 7
        assert [
                'basic-page',
                'markdown-page',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_greater_than_or_equal_to(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.filter(published__gte=on)
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_exclude_greater_than_or_equal_to(self):
        on = datetime(2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.exclude(published__gte=on)
        assert type(sources) == SourceList
        assert len(sources) == 5
        assert [
                'basic-page',
                'markdown-page',
                'series/index',
                'series/part-one',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_contains_on_string(self):
        sources = self.flourish.sources.filter(title__contains='the')
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'thing-one',
            ] == [source.slug for source in sources]

    def test_exclude_contains_on_string(self):
        sources = self.flourish.sources.exclude(title__contains='th')
        assert type(sources) == SourceList
        assert len(sources) == 7
        assert [
                'basic-page',
                'markdown-page',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_excludes_on_string(self):
        sources = self.flourish.sources.filter(title__excludes='th')
        assert type(sources) == SourceList
        assert len(sources) == 7
        assert [
                'basic-page',
                'markdown-page',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_excludes_on_string(self):
        sources = self.flourish.sources.exclude(title__excludes='th')
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'nothing',
                'thing-one',
            ] == [source.slug for source in sources]

    def test_filter_contains_on_list(self):
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should both be matched
        sources = self.flourish.sources.filter(tag__contains='basic')
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'basic-page',
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

    def test_exclude_contains_on_list(self):
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should both be excluded
        sources = self.flourish.sources.exclude(tag__contains='basic')
        assert type(sources) == SourceList
        assert len(sources) == 6
        assert [
                'markdown-page',
                'nothing',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_excludes_on_list(self):
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should both be excluded
        sources = self.flourish.sources.filter(tag__excludes='basic')
        assert type(sources) == SourceList
        assert len(sources) == 6
        assert [
                'markdown-page',
                'nothing',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_excludes_on_list(self):
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should both be matched
        sources = self.flourish.sources.exclude(tag__excludes='basic')
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'basic-page',
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

    def test_filter_contains_invalid_value(self):
        sources = self.flourish.sources.filter(published__contains='two')
        assert type(sources) == SourceList
        assert len(sources) == 0

    def test_exclude_contains_invalid_value(self):
        # trying to exclude something invalid means no exclusion takes place
        sources = self.flourish.sources.exclude(published__contains='two')
        assert type(sources) == SourceList
        assert len(sources) == 9
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_exludes_invalid_value(self):
        # trying to exclude something invalid means no exclusion takes place
        sources = self.flourish.sources.filter(published__excludes='two')
        assert type(sources) == SourceList
        assert len(sources) == 9
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_excludes_invalid_value(self):
        # trying to exclude something that excludes something invalid,
        # means the exclusion of the invalid exclusion succeeds
        sources = self.flourish.sources.exclude(published__excludes='two')
        assert type(sources) == SourceList
        assert len(sources) == 0

    def test_filter_in_list(self):
        categories = ['article', 'thing']
        sources = self.flourish.sources.filter(category__in=categories)
        assert type(sources) == SourceList
        assert len(sources) == 6
        assert [
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_in_list(self):
        categories = ['article', 'thing']
        sources = self.flourish.sources.exclude(category__in=categories)
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
            ] == [source.slug for source in sources]

    def test_filter_notin_list(self):
        categories = ['article', 'thing']
        sources = self.flourish.sources.filter(category__notin=categories)
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
            ] == [source.slug for source in sources]

    def test_exclude_notin_list(self):
        categories = ['article', 'thing']
        sources = self.flourish.sources.exclude(category__notin=categories)
        assert type(sources) == SourceList
        assert len(sources) == 6
        assert [
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_set(self):
        sources = self.flourish.sources.filter(page_type__set='')
        assert type(sources) == SourceList
        assert len(sources) == 6
        assert [
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_set(self):
        sources = self.flourish.sources.exclude(page_type__set='')
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
            ] == [source.slug for source in sources]

    def test_filter_unset(self):
        sources = self.flourish.sources.filter(page_type__unset='')
        assert type(sources) == SourceList
        assert len(sources) == 3
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
            ] == [source.slug for source in sources]

    def test_exclude_unset(self):
        sources = self.flourish.sources.exclude(page_type__unset='')
        assert type(sources) == SourceList
        assert len(sources) == 6
        assert [
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_inside_or_equal(self):
        # in contrast to test_filter_contains above,
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should not be matched
        sources = self.flourish.sources.filter(tag='basic')
        assert type(sources) == SourceList
        assert len(sources) == 0

        # ... but 'basically' should
        sources = self.flourish.sources.filter(tag='basically')
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'thing-one',
                'thing-two',
            ] == [source.slug for source in sources]

        # ... as should 'basic-page'
        sources = self.flourish.sources.filter(tag='basic-page')
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'basic-page',
            ] == [source.slug for source in sources]

    def test_exclude_inside_or_equal(self):
        # in contrast to test_filter_contains above,
        # tag='basic-page' (basic-page) and tag=['basically','...']
        # (thing-one, thing-two) should not be matched
        sources = self.flourish.sources.exclude(tag='basic')
        assert type(sources) == SourceList
        assert len(sources) == 9
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

        # ... but 'basically' should
        sources = self.flourish.sources.exclude(tag='basically')
        assert type(sources) == SourceList
        assert len(sources) == 7
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

        # ... as should 'basic-page'
        sources = self.flourish.sources.exclude(tag='basic-page')
        assert type(sources) == SourceList
        assert len(sources) == 8
        assert [
                'markdown-page',
                'nothing',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_filter_multiple_arguments(self):
        # only two sources have the tag 'two'; three of the six sources were
        # published before 12:15, three published after 12:15; filtering
        # against both of these should only find one post in each subgroup
        on = datetime(2016, 6, 4, 12, 15, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.filter(
            tag__contains='two', published__gt=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'thing-two',
            ] == [source.slug for source in sources]

        sources = self.flourish.sources.filter(
            tag__contains='two', published__lt=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'series/part-two',
            ] == [source.slug for source in sources]

        # can "stack" .filter() as well as use multiple arguments to it
        two_sources = self.flourish.sources.filter(tag__contains='two')
        sources = two_sources.filter(published__gt=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'thing-two',
            ] == [source.slug for source in sources]

        sources = two_sources.filter(published__lt=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'series/part-two',
            ] == [source.slug for source in sources]

    def test_exclude_multiple_arguments(self):
        # only two sources are not of the type 'post'; one was published
        # in 2015, one in 2016
        on = datetime(2016, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.exclude(page_type='post', published__gte=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'basic-page',
            ] == [source.slug for source in sources]

        sources = self.flourish.sources.exclude(page_type='post', published__lte=on)
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'markdown-page',
                'series/index',
            ] == [source.slug for source in sources]

        # can "stack" .filter() as well as use multiple arguments to it
        two_sources = self.flourish.sources.exclude(page_type='post')
        sources = two_sources.exclude(published__gte=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'basic-page',
            ] == [source.slug for source in sources]

        sources = two_sources.exclude(published__lte=on)
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'markdown-page',
                'series/index',
            ] == [source.slug for source in sources]

    def test_filter_then_exclude(self):
        on = datetime(2016, 6, 4, 12, 00, 00, tzinfo=timezone.utc)
        posts = self.flourish.sources.filter(page_type='post')
        sources = posts.exclude(published__gte=on)
        assert type(sources) == SourceList
        assert len(sources) == 1
        assert [
                'series/part-one',
            ] == [source.slug for source in sources]

        # other way around is the same
        sources = self.flourish.sources.exclude(published__gte=on)
        posts = sources.filter(page_type='post')
        assert type(posts) == SourceList
        assert len(posts) == 1
        assert [
                'series/part-one',
            ] == [source.slug for source in posts]

    def test_filter_and_exclude_doesnt_affect_parent(self):
        on = datetime(2016, 6, 4, 12, 15, 0, tzinfo=timezone.utc)
        filtered = self.flourish.sources.filter(
            tag__contains='two', published__gt=on)
        assert type(filtered) == SourceList
        assert len(filtered) == 1
        assert [
                'thing-two',
            ] == [source.slug for source in filtered]

        filtered_away = self.flourish.sources.exclude(page_type='post')
        assert type(filtered_away) == SourceList
        assert len(filtered_away) == 4
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'series/index',
            ] == [source.slug for source in filtered_away]

        unfiltered = self.flourish.sources.all()
        assert type(unfiltered) == SourceList
        assert len(unfiltered) == 9
        # os.walk order, root dir before subdirs, alphabetical order
        assert [
                'basic-page',
                'markdown-page',
                'nothing',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in unfiltered]

    def test_order_after_filter_works(self):
        sources = self.flourish.sources.filter(published__set='')
        assert type(sources) == SourceList
        assert len(sources) == 8
        assert [
                'basic-page',
                'markdown-page',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

        sources = sources.order_by('published')
        assert type(sources) == SourceList
        assert len(sources) == 8
        assert [
                'basic-page',
                'markdown-page',
                'series/index',
                'series/part-one',
                'series/part-two',
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_order_after_exclude_works(self):
        sources = self.flourish.sources.exclude(published__unset='')
        assert type(sources) == SourceList
        assert len(sources) == 8
        assert [
                'basic-page',
                'markdown-page',
                'thing-one',
                'thing-two',
                'series/index',
                'series/part-one',
                'series/part-three',
                'series/part-two',
            ] == [source.slug for source in sources]

        sources = sources.order_by('published')
        assert type(sources) == SourceList
        assert len(sources) == 8
        assert [
                'basic-page',
                'markdown-page',
                'series/index',
                'series/part-one',
                'series/part-two',
                'thing-one',
                'thing-two',
                'series/part-three',
            ] == [source.slug for source in sources]

    def test_filter_after_order_works(self):
        published_set = self.flourish.sources.filter(published__set='')
        sources = published_set.order_by('published')
        assert type(sources) == SourceList
        assert len(sources) == 8

        sources = sources.filter(tag__contains='one')
        assert type(sources) == SourceList
        assert len(sources) == 2
        assert [
                'series/part-one',
                'thing-one',
            ] == [source.slug for source in sources]

    def test_exclude_after_order_works(self):
        published_set = self.flourish.sources.filter(published__set='')
        sources = published_set.order_by('-published')
        assert type(sources) == SourceList
        assert len(sources) == 8

        sources = sources.exclude(series__set='')
        assert type(sources) == SourceList
        assert len(sources) == 4
        assert [
                'thing-one',
                'thing-two',
                'markdown-page',
                'basic-page',
            ] == [source.slug for source in sources]

    def test_order_after_filter_or_exclude_does_not_warn_on_absent_keys(self):
        with pytest.warns(None) as warnings:
            sources = self.flourish.sources.order_by('page_type')
            assert type(sources) == SourceList
            assert len(sources) == 9
            assert len(warnings) == 1
            assert (
                str(warnings[0].message) ==
                'sorting sources by "page_type" failed: '
                'not all sources have that attribute'
            )

        with pytest.warns(None) as warnings:
            sources = self.flourish.sources.filter(page_type='post')
            assert len(sources) == 5
            sources = sources.order_by('page_type', 'published')
            assert type(sources) == SourceList
            assert len(sources) == 5
            assert len(warnings) == 0
            assert [
                    'series/part-one',
                    'series/part-two',
                    'thing-one',
                    'thing-two',
                    'series/part-three',
                ] == [source.slug for source in sources]

        with pytest.warns(None) as warnings:
            on = datetime(2016, 6, 4, 12, 15, 0, tzinfo=timezone.utc)
            sources = self.flourish.sources.exclude(published__lt=on)
            assert len(sources) == 3
            sources = sources.order_by('page_type', '-published')
            assert type(sources) == SourceList
            assert len(sources) == 3
            assert len(warnings) == 0
            assert [
                    'series/part-three',
                    'thing-one',
                    'thing-two',
                ] == [source.slug for source in sources]

    def test_related_key_lookup(self):
        source = self.flourish.get('thing-one')
        related = source.related('line')
        assert [
            'thing-two',
        ] == [_s.slug for _s in related]

    def test_no_related_key_lookup(self):
        source = self.flourish.get('basic-page')
        related = source.related('line')
        # basic-page has no line key, so no related sources
        assert [] == [_s.slug for _s in related]

    def test_foreignkey_lookup(self):
        source = self.flourish.get('series/part-one')
        assert source.index_fkey == 'series/index'
        assert source.index.title == 'A Series in Three Parts'

    def test_foreignkey_reverse_lookup(self):
        source = self.flourish.get('series/index')
        assert [
            'series/part-one',
            'series/part-three',
            'series/part-two',
        ] == [_s.slug for _s in source.index_set]

    def test_publication_dates(self):
        all_dates = [
            {
                'year': date(2015, 1, 1),
                'months': [
                    {
                        'month': date(2015, 12, 1),
                        'days': [
                            date(2015, 12, 25),
                        ],
                    },
                ],
            },
            {
                'year': date(2016, 1, 1),
                'months': [
                    {
                        'month': date(2016, 2, 1),
                        'days': [
                            date(2016, 2, 29),
                        ],
                    },
                    {
                        'month': date(2016, 6, 1),
                        'days': [
                            date(2016, 6, 4),
                            date(2016, 6, 6),
                        ],
                    },
                ],
            },
        ]
        assert all_dates == self.flourish.publication_dates

        on = datetime(2016, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        sources = self.flourish.sources.exclude(published__lt=on)
        assert [all_dates[1]] == sources.publication_dates

        # ensure still unfiltered
        assert all_dates == self.flourish.publication_dates

class TestFlourishFuture:
    @classmethod
    def setup_class(cls):
        with pytest.warns(None) as warnings:
            cls.flourish = Flourish(
                'tests/future/source'
            )
            assert len(warnings) == 0
            assert cls.flourish.sources.count() == 4

    def test_get_all_sources(self):
        sources = self.flourish.sources.all()
        assert type(sources) == SourceList
        assert len(sources) == 4
        # os.walk order, root dir before subdirs, alphabetical order
        assert [
                'nineteenth-century',
                'twentieth-century',
                'twenty-first-century',
                'twenty-second-century',
            ] == [source.slug for source in sources]

        published = sources.order_by('-published')
        assert [
                'twenty-second-century',
                'twenty-first-century',
                'twentieth-century',
                'nineteenth-century',
            ] == [source.slug for source in published]

    def test_exclude_future(self):
        sources = self.flourish.sources.exclude_future()
        assert type(sources) == SourceList
        assert len(sources) == 3
        # os.walk order, root dir before subdirs, alphabetical order
        assert [
                'nineteenth-century',
                'twentieth-century',
                'twenty-first-century',
            ] == [source.slug for source in sources]
