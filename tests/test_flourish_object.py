import pytest

from flourish import Flourish, TomlSourceFile


class TestFlourish:
    @classmethod
    def setup_class(cls):
        cls.flourish = Flourish('tests/source')

    def test_get_all_sources(self):
        sources = self.flourish.sources.all()
        assert type(sources) == Flourish
        assert len(sources) == 4
        # os.walk order, root dir before subdirs, alphabetical order
        assert [
                'basic-page',
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
                'series/part-one',
            ] == [source.slug for source in sources]

    def test_get_sources_by_negative_slice_raises(self):
        with pytest.raises(ValueError):
            self.flourish.sources.all()[-2:2]
