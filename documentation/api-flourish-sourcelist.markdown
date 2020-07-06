[TOC]

# Flourish API: `flourish.sourcelist`


## Finding sources

```python
# everything, returned in filesystem order
for source in fl.sources.all():
    print source

# get a slice
for source in fl.sources.all()[0:2]:
    print source
```

`flourish.sources.all()` will return a list of all
[flourish.source](/api-flourish-source/) objects found in the source directory
upon initialisation.

This list can be sliced, but it does not currently support negative indicies.

### How many sources

```python
num_sources = fl.sources.count
num_posts = fl.sources.filter(type='post').count
```

The number of sources that match all
[filters](#filtering-down-to-specific-sources) currently applied.

### Individual sources

```python
about_page = fl.get('about')
```

To get one specific source by its [slug](/adding-sources/#the-slug).

### Filtering down to specific sources

```python
from datetime import datetime

posts = fl.sources.filter(type='post')
older = fl.sources.filter(published__lte=datetime(2016, 1, 1))
future = fl.sources.filter(published__gt=datetime.now())
```

The `filter` method expects one or more comparisons and returns only the
source objects that match.

The general format of the comparison is `key__operation=value`. The `key` is
the name of a key found in sources, the `operation` (separated from the key by
double underscores) is what type of comparison to perform, and the value is
what to compare the key to.

#### key/value exact match

```python
filter(key=value)
```

Given a key and a value, only sources that have that exact key/value pair will
match. For example, a source with the following TOML:

    type = 'posting'

will be matched by `filter(type='posting')` but not by `filter(type='post')`.

Does not match if the value of the key in the source is a list, even if one
item in the list is the value specified in the filter.

#### value equality

```python
filter(key__eq='value')
filter(key__neq='value')
```

Sources that have the specified value will match. The value can be inside of
a list. For example, a source with the following TOML:

    tags = ['css', 'techniques']

will be matched by `filter(tags__eq='css')` and `filter(tags__neq='html')`.

#### key exists/does not exist

```python
filter(key__set='')
filter(key__unset='')
```

To get sources that have/do not have a particular key, regardless of its
value. The value in the comparison is irrelevant for the purposes of this
filter.

#### numerical/datetime comparisons

```python
filter(key__gt=4)
filter(key__gte=5)
filter(key__lt=datetime(2000, 1, 1))
filter(key__lte=datetime(1999, 12, 31))
```

To get sources where the key has a numerical relationship to some other value:

  * `__gt` — greater than
  * `__gte` — greater than or equal to
  * `__lt` — less than
  * `__lte` — less than or equal to

#### substrings

```python
filter(key__contains='substring')
filter(key__excludes='substring')
```

To get sources where the value is (is not) a part of that source's key.

#### multiple alternatives

```python
filter(key__in=[...])
filter(key__notin=[...])
```

To get sources where the value of a key is (isn't) one of a set of many
possible values.


### Excluding sources

```python
not_posts = fl.sources.exclude(type='post')
current = fl.sources.exclude(published__gt=datetime.now())
```

Although each type of filter already has an opposite type (`eq` vs `neq`, `gt`
vs `lte`), the `exclude()` method is also available. Sometimes using it may
make illustrating the intention of some filters clearer.


## Ordering sources

```python
posts = fl.sources.filter(type='post')
posts_oldest_first = posts.order_by('published')
posts_newest_first = posts.order_by('-published')
```

Without modification, the sources returned by `all()`, `filter()` and
`exclude()` are in the order that Flourish discovered them in the filesystem.

You can alter this with `order_by()` which takes a list of strings,
representing the key(s) to sort the sources by. To reverse a sort, put a 
dash/hyphen (`-`) before the key name.

If not all matching sources have that key, a warning is issued and no
ordering takes place.


## Chaining methods together

```python
aged = datetime(2010, 1, 1)

# these are equivalent:
old_posts1 = fl.sources.filter(type='post').filter(published__lt=aged)
old_posts2 = fl.sources.filter(published__lt=aged).filter(type='post')
old_posts3 = fl.sources.filter(type='post', published__lt=aged)
old_posts4 = fl.sources.exclude(published_gte=aged).filter(type='post')
```

As you can see above, it is possible to chain the results of queries against
the source object list.
