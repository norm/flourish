# encoding: utf-8

import pytest

from flourish import Flourish
from flourish.helpers import all_valid_dates, publication_range


class TestFlourish:
    @classmethod
    def setup_class(cls):
        with pytest.warns(None) as warnings:
            cls.flourish = Flourish('tests/source')
            assert len(warnings) == 2
            assert cls.flourish.sources.count() == 8

    def test_all_valid_dates(self):
        assert [
            {
                'year': '2015',
                'months': [
                    {
                        'month': '12',
                        'days': [
                            {'day': '25'},
                        ],
                    },
                ],
            },
            {
                'year': '2016',
                'months': [
                    {
                        'month': '02',
                        'days': [
                            {'day': '29'},
                        ],
                    },
                    {
                        'month': '06',
                        'days': [
                            {'day': '04'},
                            {'day': '06'},
                        ],
                    },
                ],
            }
        ] == all_valid_dates(self.flourish)

    def test_publication_range(self):
        assert u'2015–2016' == publication_range(self.flourish)
