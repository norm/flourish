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
                'published': datetime(2015, 12, 25, 10, 00, 00),
                'title': 'Basic Page',
            } == page._config

        page = self.flourish.sources.get('series/part-one')
        assert {
                'published': datetime(2016, 06, 04, 11, 00, 00),
                'title': 'Part One',
            } == page._config

        page = self.flourish.sources.get('series/part-two')
        assert {
                'published': datetime(2016, 06, 04, 12, 00, 00),
                'title': 'Part Two',
            } == page._config
