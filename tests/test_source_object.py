# encoding: utf-8

from datetime import datetime

import pytest

from flourish import Flourish


class TestFlourishPageInvalidFrontmatter:
    def test_page_markdown_with_invalid_frontmatter(self):
        with pytest.raises(RuntimeError):
            Flourish('tests/invalid_frontmatter')


class TestFlourishPage:
    @classmethod
    def setup_class(cls):
        with pytest.warns(None) as warnings:
            cls.flourish = Flourish('tests/source')
            assert len(warnings) == 2
            assert cls.flourish.sources.count() == 7
            cls.warnings = warnings

    def test_toml_configuration(self):
        page = self.flourish.sources.get('basic-page')
        assert {
                'body': u'<p>Hello “world”.</p>',
                'category': 'static',
                'published': datetime(2015, 12, 25, 10, 00, 00),
                'tag': 'basic-page',
                'title': 'Basic Page',
            } == page._config

    def test_toml_with_inherent_markdown(self):
        page = self.flourish.sources.get('series/part-one')
        assert {
                'body_markdown': '# Part One\n\nI come from Markdown.\n',
                'body': '<h1>Part One</h1>\n\n<p>I come from Markdown.</p>\n',
                'category': 'article',
                'published': datetime(2016, 06, 04, 11, 00, 00),
                'series': 'series-in-three-parts',
                'tag': ['series', 'one'],
                'title': 'Part One',
                'type': 'post',
            } == page._config

        page = self.flourish.sources.get('thing-two')
        assert {
                'body_markdown': u'Body read from Markdown attachment‽\n',
                'body': u'<p>Body read from Markdown attachment‽</p>\n',
                'category': 'thing',
                'published': datetime(2016, 06, 04, 12, 30, 00),
                'summary_markdown': 'Thing Two summary.\n',
                'summary': '<p>Thing Two summary.</p>\n',
                'tag': ['basically', 'second', 'two'],
                'title': 'Second Thing',
                'type': 'post',
            } == page._config

    def test_toml_with_inherent_markdown_overridden_by_adherent(self):
        page = self.flourish.sources.get('series/part-three')
        assert {
                'body_markdown': '# Part Three\n\n'
                                 'The embedded Markdown gets overridden.\n',
                'body': '<h1>Part Three</h1>\n\n'
                        '<p>The embedded Markdown gets overridden.</p>\n',
                'category': 'article',
                'published': datetime(2016, 06, 06, 10, 00, 00),
                'series': 'series-in-three-parts',
                'tag': ['three', 'series'],
                'title': 'Part Three',
                'type': 'post',
            } == page._config
        # a warning is issued for this source during the initialisation of
        # Flourish, which is captured in setup_class
        assert (
            str(self.warnings[0].message) ==
            '"body_markdown" in series/part-three '
            'overriden by Markdown attachment.'
        )

    def test_toml_with_adherent_markdown(self):
        page = self.flourish.sources.get('series/part-two')
        assert {
                'body_markdown': '# Part Two\n\n'
                                 'I come from a Markdown file.\n',
                'body': '<h1>Part Two</h1>\n\n'
                        '<p>I come from a Markdown file.</p>\n',
                'category': 'article',
                'published': datetime(2016, 06, 04, 12, 00, 00),
                'series': 'series-in-three-parts',
                'tag': ['series', 'two'],
                'title': 'Part Two',
                'type': 'post',
            } == page._config
        # a warning is issued for this source during the initialisation of
        # Flourish, which is captured in setup_class
        assert (
            str(self.warnings[1].message) ==
            '"body" in series/part-two overriden by Markdown conversion.'
        )

    def test_page_markdown_with_frontmatter(self):
        page = self.flourish.sources.get('markdown-page')
        assert {
                'body_markdown': u'\n# ¡Markdown!\n\n'
                                 'I was generated from Markdown alone, '
                                 'no TOML.\n',
                'body': u'<h1>¡Markdown!</h1>\n\n'
                        '<p>I was generated from Markdown alone, '
                        'no TOML.</p>\n',
                'category': 'post',
                'published': datetime(2016, 02, 29, 10, 30, 00),
                'title': 'Plain Markdown Page',
            } == page._config

    def test_json_with_adherent_html(self):
        page = self.flourish.sources.get('thing-one')
        assert {
                'body': '<h1>Thing the First</h1>\n'
                        '<p>This is raw HTML.</p>\n',
                'category': 'thing',
                'published': datetime(2016, 06, 04, 12, 30, 00),
                'tag': ['basically', 'one', 'first'],
                'title': u'Thing—the First',
                'type': 'post',
                'updated': datetime(2016, 06, 04, 14, 00, 00),
            } == page._config
