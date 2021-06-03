# Flourish API: `flourish.generators.atom.AtomGenerator`

`AtomGenerator` is the class for generating an Atom feed of sources.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).

```python
from flourish.generators import atom

PATHS = (
    ...
    atom.AtomGenerator(
        name = 'atom-feed',
        path = '/index.atom',
    ),
    ...
)

```


## Class attributes

  * `limit` — This generator should return no more than `limit` sources.
    Default value is `20`. Set to `None` to return all sources.
  * `order_by` — This generator should sort matching sources in this way.
    Default value is `-published` (most-recent first).
  * `sources_exclude` — This generator should exclude sources that match
    this filter. Default value is `None`.
  * `sources_filter` — This generator should only use sources that match
    this filter; see
    [Filtering down to specific sources](/api-flourish/#filtering-down-to-specific-sources).
    Default value is `None`.


## Methods

### get_objects(tokens)

Returns only sources that have a `published` key set to datetime value that
is before now (ie. anything declared to be published "in the future") will
not be included in the Atom feed.

### render_output()

Bypasses `get_context_data`, `get_template`, `get_template_name` and 
`render_template`, instead constructing the Atom feed programmatically
using the `FeedGenerator` class provided by [feedgen], calling
`get_feed_author`, `get_feed_title`, and for every entry, `get_entry_author`,
`get_entry_content`, `get_entry_title`, and `get_entry_id`.

[feedgen]: https://pypi.python.org/pypi/feedgen

### get_feed_author()

Return the Atom feed's author. By default it is the value of `author` from
the site config.

### get_feed_title()

Return the Atom feed's title. By default it is the value of `title` from
the site config.

### get_entry_author(object)

Return the Atom entry's author. By default it is the value of `author` from
the site config.

### get_entry_content(object)

Return the Atom entry's content. By default just the source object's body.

### get_entry_title(object)

Return the Atom entry's title. By default the source object's title.

### get_entry_id(object)

Return the Atom entry's ID. By default the source object's URL.

### get_context_data()

Not called.

### get_template()

Not called.

### get_template_name()

Not called.

### render_template(template, context_data)

Not called.
