import pytest

from flourish import Flourish, TomlSourceFile


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
