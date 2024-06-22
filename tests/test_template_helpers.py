# encoding: utf-8

import warnings

from flourish import Flourish
from flourish.helpers import publication_range


class TestFlourish:
    @classmethod
    def setup_class(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cls.flourish = Flourish('tests/source')

    def test_publication_range(self):
        assert u'2015–2016' == publication_range(self.flourish)
