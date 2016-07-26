# AtomGenerator

`AtomGenerator` is the class for generating an Atom feed of sources.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).


## Class attributes

  * `limit` — This generator should return no more than `limit` sources.


## Methods

### get_objects(tokens)

Returns only sources that have a `published` key set to datetime value that
is before now (ie. anything declared to be published "in the future") will
not be included in the Atom feed.

The sources are sorted most-recent first.

### render_output()

Bypasses `get_context_data`, `get_template`, `get_template_name` and 
`render_template`, instead constructing the Atom feed programmatically
using the `AtomFeed` class provided by [pyatom].

[pyatom]: https://pypi.python.org/pypi/pyatom

### get_context_data()

Not called.

### get_template()

Not called.

### get_template_name()

Not called.

### render_template(template, context_data)

Not called.
