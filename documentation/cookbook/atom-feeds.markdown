# Adding Atom feeds to your site

You can add an Atom feed (which is used identically to RSS) to your site,
containing all sources with a `published` timestamp that is before now
(published dates in the future are not considered "published" and so don't
appear in the feed).

Before you add a feed, the [site configuration file](/site-configuration/)
will need three entries added, which are used in the header of Atom feeds:

```python
author = 'Wendy Testaburger'
base_url = 'http://example.com'
title = 'Blog'
```

Ensure each source which should appear in the feed has at least the
following entries:

```python
title = "Blog post about things"
published = 2016-06-30T13:30:00Z
```

Then add this at the top of your [generation script](/generating-the-site/):

```python
from flourish.generators.atom import AtomGenerator
```

then below, add this to your list of `PATHS`:

```python
    AtomGenerator(
        path = '/index.atom',
        name = 'site-atom-feed',
    ),
```

Regenerate the site and upload it and you should have an Atom feed.
