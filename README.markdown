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

Any source TOML file can have one or more Markdown blocks added to it
if they share the same slug part of the filename. For example, a
`blog-post.toml` file will read in `blog-post.summary.markdown` as
though it were specified as the key `summary_markdown` in the TOML.

Any key in the resulting source configuration that ends `_markdown`
will be converted to HTML, eg `body_markdown` is converted and the 
result stored in `body`.

```toml
# example TOML file with 
body_markdown = """
# Part One

I come from Markdown.
"""
body = 'I get replaced with HTML created from `body_markdown` above'
category = 'article'
published = 2016-06-04T11:00:00Z
series = 'series-in-three-parts'
tag = ['series', 'one']
title = 'Part One'
type = 'post'
```


Usage
-----

Currently, flourish doesn't actually generate anything, it is still in
development.

```python
from datetime import datetime
from flourish import Flourish

source_dir = 'tests/source'
fl = Flourish(source_dir)

# get everything, in filesystem order
for source in fl.sources.all():
    print source

# get everything in reverse order of 'publication'
for source in fl.sources.all().order_by('-published')
    print source

# get a slice
for source in fl.sources.all()[0:2]:
    print source

# get one thing by "slug" (its filename minus .toml)
print fl.sources.get('series/part-one')

# get sources by attribute
posts = fl.sources.filter(type='post')
older = fl.sources.filter(published__lte=datetime(2016, 1, 1))
future = fl.sources.filter(published__gt=datetime.now())
twos = fl.sources.filter(tag__contains='two')
series = fl.sources.filter(series__set='')
```



[toml]: https://github.com/toml-lang/toml
[cbv]: https://docs.djangoproject.com/en/stable/topics/class-based-views/
[dfbo]: https://github.com/jaylett/django-filebacked-objects
