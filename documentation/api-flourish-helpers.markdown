[TOC]

# Template helpers

## Get the publication year range

```python
from flourish.helpers import publication_range

publication_range(flourish, 'updated')
```

`publication_range(flourish, key)` will return a string like `2012–2016`,
for the years of any source that has a datetime in `key`. This is useful for
creating the copyright line in a site's footer.

The first argument is your flourish instance.

The second argument is which key to use to find the dates. It is optional, and
the default is `'published'` (which is one of the 
[special keys](/adding-sources/#special-keys-in-sources) in Flourish).
