# Linking sources together

You can create relationships between sources in various ways, if you need
to establish that they are connected.

## Common keys

If the sources share a key/value pair, you can find other sources with the
`related` method on the source. For example, if you collect articles using a
key `series`, this code will get the other articles in the same series:

```html
<h3>Related articles</h3>
<ul id='related'>
  {% for related in page.related('series') %}
    <li><a href='{{related.url}}'>{{related.title}}</a></li>
  {% endfor %}
</ul>
```


## Foreign key lookups

Mimicking a [one-to-many relationship][o2m] from databases, any key in a
source that ends `_fkey` can be used to lookup another source directly. When
using it, you should refer to the key without the extension. For example,
given a source `advanced-bbq` with the following content excerpt:

```python
parent_fkey = 'basic-bbq'
```

and a source `basic-bbq` with the following content excerpt:

```python
title = 'Getting started with BBQ'
```

then the following template fragment in the context of the `advanced-bbq`:

```html
<p>
  Make sure you've read
  <a href='{{page.parent.url}}'>{{page.parent.title}}</a>
  first!
</p>
```

would render as:

```html
<p>
  Make sure you've read
  <a href='/basic-bbq'>Getting started with BBQ</a>
  first!
</p>
```

[o2m]: https://en.wikipedia.org/wiki/One-to-many_(data_model)

## Reverse foreign key lookups

Once a source or sources use the foreign key lookup mechanism, the source
they refer to can get at the sources that link to it, by using the same 
key as used to link to it (the one that ends `_fkey`) and appending `_set`.

To extend the above example, in the template for the `advanced-bbq` source,
the following code would create links to all sources using `index_fkey` to
reference it.

```html
<h2>Articles that link to this</h2>
<ul>
  {% for child in page.parent_set %}
    <li><a href='{{child.url}}'>{{child.title}}</a></li>
  {% endfor %}
</ul>
```
