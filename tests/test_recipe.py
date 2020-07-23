from textwrap import dedent

import pytest

from flourish import Flourish
from flourish.sourcelist import SourceList


class TestRecipe:
    def test_recipe_file_templates(self):
        with pytest.warns(None) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                templates_dir='tests/templates',
            )
            assert len(warnings) == 2

        recipe = flourish.path_recipe('/')
        assert recipe['path'] == '/'
        assert recipe['template_name'] == 'index.html'

        expected_template = dedent("""\
            {% extends "base.html" %}

            {% block body %}
              <ul>
                {% for page in pages %}
                  <li>
                    <a href='{{page.path}}'>{{page.title}}</a>
                  </li>
                {% endfor %}
              </ul>

              {% if pagination %}
                <ul class='pagination'>
                  {% for page in pagination %}
                    <li>
                      {% if page.number == current_page.number %}
                        <em>Page {{page.number}}</em>
                      {% else %}
                        <a href='{{page.path}}'>Page {{page.number}}</a>
                      {% endif %}
                    </li>
                  {% endfor %}
                </ul>
              {% endif %}
            {% endblock %}
        """)
        assert recipe['template'] == expected_template

        context_contains = {
            'global': {'copyright_year_range': '2015–2016'},
            'site': {'author': 'Wendy Testaburger',
                     'base_url': 'http://withaflourish.net',
                     'title': 'Flourish Blog'},
            'tokens': {},
        }
        print(recipe)
        assert recipe['context'].items() >= context_contains.items()
        assert type(recipe['context']['sources']) == SourceList
        assert recipe['context']['sources'].count() == 8
        assert type(recipe['context']['pages']) == SourceList
        assert recipe['context']['pages'].count() == 8

    def test_recipe_sectile_templates(self):
        with pytest.warns(None) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                fragments_dir='tests/fragments',
            )
            assert len(warnings) == 2

        recipe = flourish.path_recipe('/')
        assert recipe['path'] == '/'
        assert recipe['template_name'] == 'index.html'

        expected_template = dedent("""\
            <html lang='en-GB'>
            <head>
              <meta charset='UTF-8'>
              <title>{{title}}</title>
            </head>
            <body class=''>

            <header>
              <nav>
                <ul>
                  <li><a href='{{ path("homepage") }}'>Homepage</a></li>
                  <li><a href='{{ path("atom-feed") }}'>Atom Feed</a></li>
                  <li><a href='{{ path("tags-tag-page", tag="css") }}'>Posts tagged CSS</a></li>
                </ul>
              </nav>
            </header>


              <ul>
                {% for page in pages %}
                  <li>
                    <a href='{{page.path}}'>{{page.title}}</a>
                  </li>
                {% endfor %}
              </ul>

              {% if pagination %}
                <ul class='pagination'>
                  {% for page in pagination %}
                    <li>
                      {% if page.number == current_page.number %}
                        <em>Page {{page.number}}</em>
                      {% else %}
                        <a href='{{page.path}}'>Page {{page.number}}</a>
                      {% endif %}
                    </li>
                  {% endfor %}
                </ul>
              {% endif %}



            <footer>
              <p>Copyright {{global.copyright_year_range}} {{site.author}}.</p>
            </footer>

            </body>
            </html>
        """)
        assert recipe['template'] == expected_template

        context_contains = {
            'global': {'copyright_year_range': '2015–2016'},
            'site': {'author': 'Wendy Testaburger',
                     'base_url': 'http://withaflourish.net',
                     'title': 'Flourish Blog'},
            'tokens': {},
        }
        assert recipe['context'].items() >= context_contains.items()
        assert type(recipe['context']['sources']) == SourceList
        assert recipe['context']['sources'].count() == 8
        assert type(recipe['context']['pages']) == SourceList
        assert recipe['context']['pages'].count() == 8

        expected_fragments = [
            {'depth': 0, 'index.html': 'default/index.html'},
            {'depth': 1, 'base.html': 'default/base.html'},
            {'depth': 2, 'head_wrapper': 'default/head_wrapper'},
            {'depth': 2, 'body_wrapper': 'default/body_wrapper'},
            {'depth': 3, 'body_class': None},
            {'depth': 3, 'body': 'index/all/body'},
            {'depth': 3, 'related': None},
        ]
        assert recipe['sectile_fragments'] == expected_fragments
        assert recipe['sectile_dimensions'] == {'generator': 'homepage'}
