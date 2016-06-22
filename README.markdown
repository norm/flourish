flourish
========

A static site generator built around the idea that combining Markdown files
and templates is **not enough** for anything but the most basic needs, and
that enabling plugins is mostly a panacea for being able to really develop
functionality that is site specific.

Heavily inspired by django's [class based views][cbv] and James Aylett's
[django file-backed objects][dfbo].


How it works
------------
Flourish first gathers all [TOML][toml] files found under a source directory
and allows this to be iterated and queried for individual items.


Usage
-----

Currently, flourish doesn't actually generate anything, it is still in
development.

    from flourish import Flourish

    source_dir = 'tests/source'
    fl = Flourish(source_dir)

    # get everything
    for source in fl.sources.all():
        print source

    # get a slice
    for source in fl.sources.all()[0:2]:
        print source

    # get one thing by "slug" (its filename minus .toml)
    print fl.sources.get('series/part-one')



[toml]: https://github.com/toml-lang/toml
[cbv]: https://docs.djangoproject.com/en/stable/topics/class-based-views/
[dfbo]: https://github.com/jaylett/django-filebacked-objects
