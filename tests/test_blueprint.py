from textwrap import dedent, indent

import pytest

from flourish import Flourish
from flourish.sourcelist import SourceList


class TestBlueprint:
    def test_blueprint_resources_imported(self):
        from flourish import blueprint
        assert blueprint.toolbar
        assert blueprint.template

    def test_blueprint_file_templates(self):
        with pytest.warns(None) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                templates_dir='tests/templates',
            )

        blueprint = flourish.path_blueprint('/')
        assert blueprint['path'] == '/'
        assert blueprint['template_name'] == 'index.html'

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
        assert blueprint['template'] == expected_template

        context_contains = {
            'global': {'copyright_year_range': '2015–2016'},
            'site': {'author': 'Wendy Testaburger',
                     'base_url': 'http://withaflourish.net',
                     'title': 'Flourish Blog',
                     'future': False},
            'tokens': {},
        }
        assert blueprint['context'].items() >= context_contains.items()
        assert type(blueprint['context']['sources']) == SourceList
        assert blueprint['context']['sources'].count() == 8
        assert type(blueprint['context']['pages']) == SourceList
        assert blueprint['context']['pages'].count() == 8
        assert blueprint['debug_page_context'] == dedent("""\
            {
              "site": {
                "author": "Wendy Testaburger",
                "base_url": "http://withaflourish.net",
                "title": "Flourish Blog",
                "future": false
              },
              "tokens": {},
              "generator": "homepage",
              "sources": {
                "sources": null,
                "ordering": [
                  "-published"
                ],
                "filters": [
                  [
                    "published__set",
                    ""
                  ]
                ],
                "slice": null,
                "future": false
              },
              "pages": {
                "sources": null,
                "ordering": [
                  "-published"
                ],
                "filters": [
                  [
                    "published__set",
                    ""
                  ]
                ],
                "slice": null,
                "future": false
              }
            }""")
        assert blueprint['debug_global_context'] == dedent("""\
            {
              "copyright_year_range": "2015\\u20132016"
            }""")


    def test_blueprint_sectile_templates(self):
        with pytest.warns(None) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                fragments_dir='tests/fragments',
            )

        blueprint = flourish.path_blueprint('/')
        assert blueprint['path'] == '/'
        assert blueprint['template_name'] == 'index.html'

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
        """)  # noqa: E501
        assert blueprint['template'] == expected_template

        context_contains = {
            'global': {'copyright_year_range': '2015–2016'},
            'site': {'author': 'Wendy Testaburger',
                     'base_url': 'http://withaflourish.net',
                     'title': 'Flourish Blog',
                     'future': False},
            'tokens': {},
        }
        assert blueprint['context'].items() >= context_contains.items()
        assert type(blueprint['context']['sources']) == SourceList
        assert blueprint['context']['sources'].count() == 8
        assert type(blueprint['context']['pages']) == SourceList
        assert blueprint['context']['pages'].count() == 8

        with open('tests/fragments/index/all/body', 'r') as handle:
            body = handle.read()
        with open('tests/fragments/default/body_wrapper', 'r') as bw_handle:
            body_wrapper = bw_handle.read()

        expected_fragments = [
            {
                'depth': 0,
                'dimensions': {
                    'generator': 'all',
                    'page_type': 'all',
                    'path': 'index.html',
                },
                'file': 'index.html',
                'found': 'default/index.html',
                'fragment': '[[ sectile insert base.html ]]\n',
            },
            {
                'depth': 1,
                'dimensions': {
                    'generator': 'all',
                    'page_type': 'all',
                    'path': 'base.html',
                },
                'file': 'base.html',
                'found': 'default/base.html',
                'fragment': (
                    "<html lang='en-GB'>\n"
                    '[[ sectile insert head_wrapper ]]\n'
                    '[[ sectile insert body_wrapper ]]\n'
                    '</html>\n'
                ),
            },
            {
                'depth': 2,
                'dimensions': {
                    'generator': 'all',
                    'page_type': 'all',
                    'path': 'head_wrapper',
                },
                'file': 'head_wrapper',
                'found': 'default/head_wrapper',
                'fragment': dedent("""\
                    <head>
                      <meta charset='UTF-8'>
                      <title>{{title}}</title>
                    </head>
                    """),
            },
            {
                'depth': 2,
                'dimensions': {
                    'generator': 'all',
                    'page_type': 'all',
                    'path': 'body_wrapper',
                },
                'file': 'body_wrapper',
                'found': 'default/body_wrapper',
                'fragment': body_wrapper,
            },
            {
                'depth': 3,
                'dimensions': {
                    'generator': None,
                    'page_type': None,
                    'path': None,
                },
                'file': 'body_class',
                'found': None,
                'fragment': '',
            },
            {
                'depth': 3,
                'dimensions': {
                    'generator': 'index',
                    'page_type': 'all',
                    'path': 'body',
                },
                'file': 'body',
                'found': 'index/all/body',
                'fragment': body,
            },
            {
                'depth': 3,
                'dimensions': {
                    'generator': None,
                    'page_type': None,
                    'path': None,
                },
                'file': 'related',
                'found': None,
                'fragment': '',
            },
        ]
        assert blueprint['sectile_fragments'] == expected_fragments
        assert blueprint['sectile_dimensions'] == {
            'generator': 'homepage',
            'page_type': 'all',
        }
        assert blueprint['debug_page_context'] == dedent("""\
            {
              "site": {
                "author": "Wendy Testaburger",
                "base_url": "http://withaflourish.net",
                "title": "Flourish Blog",
                "future": false
              },
              "tokens": {},
              "generator": "homepage",
              "sources": {
                "sources": null,
                "ordering": [
                  "-published"
                ],
                "filters": [
                  [
                    "published__set",
                    ""
                  ]
                ],
                "slice": null,
                "future": false
              },
              "pages": {
                "sources": null,
                "ordering": [
                  "-published"
                ],
                "filters": [
                  [
                    "published__set",
                    ""
                  ]
                ],
                "slice": null,
                "future": false
              }
            }""")
        assert blueprint['debug_global_context'] == dedent("""\
            {
              "copyright_year_range": "2015\\u20132016"
            }""")
