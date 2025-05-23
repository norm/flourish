# encoding: utf-8

from datetime import datetime, timezone

import pytest
import warnings

from flourish import Flourish


class TestFlourishPageInvalidFrontmatter:
    def test_page_markdown_with_invalid_frontmatter(self):
        with pytest.raises(RuntimeError):
            Flourish('tests/invalid_frontmatter')


class TestFlourishPage:
    @classmethod
    def setup_class(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cls.flourish = Flourish('tests/source')

    def test_toml_configuration(self):
        page = self.flourish.get('basic-page')
        assert {
                'body': u'<p>Hello “world”.</p>',
                'category': 'static',
                'published': datetime(
                    2015, 12, 25, 10, 0, 0, tzinfo=timezone.utc),
                'tag': 'basic-page',
                'title': 'Basic Page',
                'previous_slug': [
                    '/page',
                ],
            } == page._config

    def test_toml_with_inherent_markdown(self):
        page = self.flourish.get('series/part-one')
        assert {
                'body_markdown': '# Part One\n\nI come from Markdown.\n',
                'body': '<h1>Part One</h1>\n\n<p>I come from Markdown.</p>\n',
                'category': 'article',
                'index_fkey': 'series/index',
                'published': datetime(
                    2016, 6, 4, 11, 0, 0, tzinfo=timezone.utc),
                'series': 'series-in-three-parts',
                'tag': ['series', 'one'],
                'title': 'Part One',
                'page_type': 'post',
            } == page._config

        page = self.flourish.get('thing-two')
        assert {
                'body_markdown': u'Body read from Markdown attachment‽\n',
                'body': u'<p>Body read from Markdown attachment‽</p>\n',
                'category': 'thing',
                'line': 'two-things',
                'published': datetime(
                    2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc),
                'summary_markdown': 'Thing Two summary.\n',
                'summary': '<p>Thing Two summary.</p>\n',
                'tag': ['basically', 'second', 'two'],
                'title': 'Second Thing',
                'page_type': 'post',
            } == page._config

    def test_toml_with_inherent_markdown_overridden_by_adherent(self):
        page = self.flourish.get('series/part-three')
        assert {
                'body_markdown': '# Part Three\n\n'
                                 'The embedded Markdown gets overridden.\n',
                'body': '<h1>Part Three</h1>\n\n'
                        '<p>The embedded Markdown gets overridden.</p>\n',
                'category': 'article',
                'index_fkey': 'series/index',
                'published': datetime(
                    2016, 6, 6, 10, 0, 0, tzinfo=timezone.utc),
                'series': 'series-in-three-parts',
                'tag': ['three', 'series'],
                'title': 'Part Three',
                'page_type': 'post',
            } == page._config

    def test_toml_with_adherent_markdown(self):
        page = self.flourish.get('series/part-two')
        assert {
                'body_markdown': '# Part Two\n\n'
                                 'I come from a Markdown file.\n',
                'body': '<h1>Part Two</h1>\n\n'
                        '<p>I come from a Markdown file.</p>\n',
                'category': 'article',
                'index_fkey': 'series/index',
                'published': datetime(
                    2016, 6, 4, 12, 0, 0, tzinfo=timezone.utc),
                'series': 'series-in-three-parts',
                'tag': ['series', 'two'],
                'title': 'Part Two',
                'page_type': 'post',
            } == page._config

    def test_page_markdown_with_frontmatter(self):
        page = self.flourish.get('markdown-page')
        assert {
                'body_markdown': u'\n\n# ¡Markdown!\n\n'
                                 'I was generated from Markdown alone, '
                                 'no TOML.\n',
                'body': u'<h1>¡Markdown!</h1>\n\n'
                        '<p>I was generated from Markdown alone, '
                        'no TOML.</p>\n',
                'category': 'post',
                'published': datetime(
                    2016, 2, 29, 10, 30, 0, tzinfo=timezone.utc),
                'title': 'Plain Markdown Page',
            } == page._config

    def test_json_with_adherent_html(self):
        page = self.flourish.get('thing-one')
        assert {
                'body': '<h1>Thing the First</h1>\n'
                        '<p>This is raw HTML.</p>\n',
                'category': 'thing',
                'line': 'two-things',
                'published': datetime(
                    2016, 6, 4, 12, 30, 0, tzinfo=timezone.utc),
                'tag': ['basically', 'one', 'first'],
                'title': u'Thing—the First',
                'page_type': 'post',
                'updated': datetime(
                    2016, 6, 4, 14, 0, 0, tzinfo=timezone.utc),
            } == page._config
