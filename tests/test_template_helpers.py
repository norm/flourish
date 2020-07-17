# encoding: utf-8

import pytest

from flourish import Flourish
from flourish.helpers import publication_range


class TestFlourish:
    @classmethod
    def setup_class(cls):
        with pytest.warns(None) as warnings:
            cls.flourish = Flourish('tests/source')
            assert len(warnings) == 2
            assert cls.flourish.sources.count() == 9

    def test_publication_range(self):
        assert u'2015–2016' == publication_range(self.flourish)
