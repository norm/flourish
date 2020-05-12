"""
The example files that are created by running `flourish start`
on the command-line.
"""

from textwrap import dedent


example_files = {
    'source/_site.toml': dedent("""\
        author = 'Your Name Goes Here'
        base_url = 'http://example.com'
        title = 'Your New Flourish Blog'
    """),

    'source/generate.py': dedent("""\
        from flourish import helpers
        from flourish.generators import (
            IndexGenerator,
            PageGenerator,
        )


        class Homepage(IndexGenerator):
            order_by = ('published')
            template_name = 'homepage.html'


        def global_context(self):
            return {
                'dates': helpers.all_valid_dates(self.flourish),
            }

        GLOBAL_CONTEXT = global_context


        SOURCE_URL = (
            '/#slug',
            PageGenerator.as_generator(),
        )

        URLS = (
            (
                '/',
                'homepage',
                Homepage.as_generator()
            ),
            (
                '/#year/',
                'year-index',
                IndexGenerator.as_generator()
            ),
            (
                '/#year/#month',
                'month-index',
                IndexGenerator.as_generator()
            ),
        )
    """),

    'source/adding-pages.markdown': dedent("""\
        ---
        title = 'Adding pages'
        published = 2016-07-01T10:00:00Z
        ---

        Now let's add a new post to your blog. Using your text editor, create a
        new file called `learn-more-about-flourish.markdown` in the `source`
        directory, then copy and paste the text below into it:

            ---
            title = 'Learn more about Flourish'
            published = 2016-07-02T10:00:00Z
            ---

            This example site is a very brief introduction to using Flourish. For
            more information check out the [Flourish documentation][fd].

            If you find a problem, please file an [issue on GitHub][ish].

            To chat with other people who use Flourish, join [the Flourish Slack][slack].

            And you can follow [Flourish on twitter][tw] for updates.


            [fd]: http://withaflourish.net
            [ish]: https://github.com/norm/flourish/issues
            [slack]: http://slack.withaflourish.net
            [tw]: https://twitter.com/flourishpy

        Once you have saved this new post, click on the site header to return to the
        homepage. You'll notice that a new link has appeared ("Learn more about
        Flourish"). Click on this new post to continue.
    """),   # noqa: E501

    'source/editing-the-site.markdown': dedent("""\
        ---
        title = 'Editing the site'
        published = 2016-06-30T10:00:00Z
        tag = 'editing'
        ---

        To learn more about editing a Flourish powered web site, first open the
        directory you ran `flourish example` in into your text editor. Open the file
        `editing-the-site.markdown` in the `source` directory. This file contains
        Markdown that Flourish uses to create the web page you are reading.

        Add, change or delete some of the words in this paragraph, save the file
        and reload the page in your browser to see the changes take effect. When you
        are creating the content for your new Flourish site, this is how you can
        preview it as you write.

        ## Changing the site-wide configuration

        There is a file `_site.toml` in the `source` directory. It is not the source
        for any specific page, but rather it is site-wide configuration.

        Open it in your text editor and change the text "Your Name Goes Here" to
        contain your name, save the file, reload this webpage and scroll to the
        bottom. You'll see your name appear in the copyright statement in the footer.

        Now you have a flavour of how to see your changes take effect,
        let's [add a new page](/adding-pages).
    """),   # noqa: E501

    'source/welcome.markdown': dedent("""\
        ---
        title = 'Welcome to your new blog'
        published = 2016-06-29T10:00:00Z
        ---

        Welcome to your new blog, powered by Flourish. This example content will
        walk you through the basics of getting started using Flourish.

        Try clicking around the site. See how the title at the top of the page always
        takes you to the homepage and that there are three posts linked from there;
        that "2016" takes you to a similar list of pages, but the "06" and "07" links
        show less links? These links are all programmatically generated from the
        site's source.

        The homepage links to all pages, the "2016" page links to all pages published
        in the year 2016, and "06" and "07" link to pages published in June and July
        of that year.

        Having familiarised yourself with the site as it is now, let's start
        [editing it!](/editing-the-site)
    """),   # noqa: E501

    'source/site.css': dedent("""\
        body {
            max-width: 600px;
            margin: 2em auto;
            font-size: 1.2em;
            line-height: 1.4;
        }

        header {
            margin: 0 -40px 0;
            padding: 0 40px;
            border-bottom: 1px solid #ccc;
        }
        header h1,
        header p {
            font-size: 1.25em;
            font-weight: bold;
        }

        header nav {
            padding: 0;
            margin: 0 0 1em;
        }
        header nav ul, header nav li {
            padding: 0;
            margin: 0;
            list-style: none;
        }
        header nav li ul, header nav li li {
            display: inline-block;
        }
        header nav ul ul li:after {
            content: ', ';
        }
        header nav ul ul li:last-child:after {
            content: '';
        }

        #posts {
            margin: 2em 0;
            padding: 0;
        }
        #posts li {
            margin: 0 0 2em;
            padding: 0;
            list-style: none;
        }
        #posts li time {
            color: #666;
            display: block;
        }
        #posts li a {
            font-size: 1.5em;
        }

        pre {
            margin: 0 1em;
            padding: 0.5em 1em;
            overflow: scroll;
            background: #dee;
            border: 1px solid #599;
        }
        code {
            color: #266;
            background: #dee;
        }
        p > code {
            border: 1px solid #599;
            display: inline-block;
            padding: 1px 3px;
            line-height: 1.2;
        }

        footer {
            margin: 4em -40px 2em;
            padding: 0 40px;
            border-top: 1px solid #ccc;
        }
    """),

    'templates/base.html': dedent("""\
        <html lang='en-GB'>
        <head>
          <meta charset='UTF-8'>
          <title>{{title}}</title>
          <link rel='stylesheet' href='/site.css'>
        </head>
        <body>

        <header>
          {% block header %}
            <p>
              <a href='/'>
               {{site.title}}
              </a>
            </p>
          {% endblock %}

          <nav>
            <ul>
              {% for year in global.dates %}
                <li>
                  <a href='/{{year.year}}/'>{{year.year}}</a>:
                  <ul>
                    {% for month in year.months %}
                      <li><a href='/{{year.year}}/{{month.month}}'>{{month.month}}</a></li>
                    {% endfor %}
                  </ul>
                </li>
              {% endfor %}
            </ul>
          </nav>
        </header>


        <div id='body'>
          {% block body %}{% endblock %}
        </div>

        <footer>
          <p>
            Copyright &copy; 2016 {{site.author}}.
            Site made <a href='http://withaflourish.net'>with a flourish</a>.
          </p>
        </footer>

        </body>
        </html>
    """),   # noqa: E501

    'templates/homepage.html': dedent("""\
        {% extends "index.html" %}

        {% block header %}
          <h1>{{site.title}}</h1>
        {% endblock %}
    """),

    'templates/index.html': dedent("""\
        {% extends "base.html" %}

        {% block body %}

          <ul id='posts'>
            {% for page in pages %}
              <li>
                {% if page.published %}
                  <time datetime='{{page.published.strftime("%Y-%m-%dT%H:%M:%SZ")}}'>
                    {{page.published.strftime('%A %B %d, %Y')}}
                  </time>
                {% endif %}
                <a href='{{page.url}}'>{{page.title}}</a>
              </li>
            {% endfor %}
          </ul>

        {% endblock %}
    """),   # noqa: E501

    'templates/page.html': dedent("""\
        {% extends "base.html" %}

        {% block body %}

          <h1>{{page.title}}</h1>
          {{page.body}}

        {% endblock %}
    """),
}
