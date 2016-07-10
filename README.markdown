# flourish
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

```bash
pip install flourish
mkdir example
cd example
flourish example
```

## Documentation

Full documentation is available on [Read the Docs][rtd].

[rtd]: http://flourish.readthedocs.io/en/latest/
