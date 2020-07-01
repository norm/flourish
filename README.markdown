![Run tests](https://github.com/norm/flourish/workflows/Run%20tests/badge.svg)

Flourish
========

Flourish is a static website generator. It can be used to create a blog or
journal, a photo gallery, a portfolio, documentation, and any other kind of
website — as long as the pages should always be the same no matter when, who,
how, or what, is viewing them.

By separating your content ("source") from the HTML ("template"), you can
focus more on the adding of new content than on the act of wrangling web
pages. Further, because your content can be written in [Markdown][md] rather
than HTML, you can concentrate on just your content, on just your words, and
let the website take care of itself.

It is designed around the ideas that:

  * only combining your content with predefined themes is limiting for
    any site but the most basic
  * plugins are stop-gap solution and often don't work the way you want,
    making you change your pages and designs to fit the plugin
  * if you have specific requirements on how the site should work, you should
    not be held back

Whilst being perfectly useful for non-programmers, Flourish really shines in
the hands of developers who can write python. It can create almost any
content, and be setup to create webpages in almost any way.

It is heavily inspired by django's [class based views][cbv] and James Aylett's
[django file-backed objects][dfbo].

[md]: http://daringfireball.net/projects/markdown/
[cbv]: https://docs.djangoproject.com/en/stable/topics/class-based-views/
[dfbo]: https://github.com/jaylett/django-filebacked-objects


## Quick start

Flourish is installable from [pypi][pypi].

```bash
pip install flourish
mkdir example
cd example
flourish example
```

[pypi]: https://pypi.python.org/pypi/flourish


## Documentation

The Flourish documentation is available on [Read the Docs][rtd].

There is also a (very quiet and empty) [Slack][slack] for users of Flourish.

[rtd]: https://flourish.readthedocs.io/en/latest/
[slack]: http://slack.withaflourish.net


## TODOs

Outstanding work is mostly kept in GitHub Issues (or as `FIXME`s and `TODO`s
in the code where I've been lazy, or they don't introduce new features). 

Things that will be added in the near future are listed in Issues, tagged with
[the 1.0 milestone][1].

Things that will be added in the longer term are listed in Issues, tagged with
[the 2.0 milestone][2].

Things I'll probably never get around to are listed in Issues, tagged
[Pie in the Sky][pie].

Anything in Issues [without a milestone][bugs] is probably a bug reported by
lovely people trying to improve Flourish.

[1]: https://github.com/norm/flourish/milestone/1
[2]: https://github.com/norm/flourish/milestone/2
[pie]: https://github.com/norm/flourish/milestone/3
[bugs]: https://github.com/norm/flourish/issues?q=is%3Aopen+is%3Aissue+no%3Amilestone
