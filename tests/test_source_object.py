from datetime import datetime

import pytest

from flourish import Flourish



class TestFlourishPage:
    @classmethod
    def setup_class(cls):
        cls.flourish = Flourish('tests/source')

    def test_toml_configuration(self):
        page = self.flourish.sources.get('basic-page')
        assert {
                'category': 'static',
                'published': datetime(2015, 12, 25, 10, 00, 00),
                'tag': 'basic-page',
                'title': 'Basic Page',
            } == page._config

        page = self.flourish.sources.get('series/part-one')
        assert {
                'category': 'article',
                'published': datetime(2016, 06, 04, 11, 00, 00),
                'series': 'series-in-three-parts',
                'tag': ['series', 'one'],
                'title': 'Part One',
                'type': 'post',
            } == page._config

        page = self.flourish.sources.get('series/part-two')
        assert {
                'category': 'article',
                'published': datetime(2016, 06, 04, 12, 00, 00),
                'series': 'series-in-three-parts',
                'tag': ['series', 'two'],
                'title': 'Part Two',
                'type': 'post',
            } == page._config
