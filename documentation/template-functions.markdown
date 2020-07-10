# Template functions

There are functions made available for use in templates.


## Resolving paths

If you hardcode paths in links in your templates, you are forcing yourself to
edit multiple files if/when you change the path. Rather than hardcoding paths
in your templates you can use the `path()` function, like so:

```html
<nav>
  <ul>
    <li><a href='{{ path("homepage") }}'>Homepage</a></li>
    <li><a href='{{ path("tag-index", tag="css") }}'>Pages tagged CSS</a></li>
  </ul>
</nav>
```

The first argument is the [symbolic name of the path](/adding-paths/) as defined
in your `PATHS` list. If the path requires any 
[replacable tokens](/adding-paths/#url-paths) those come after the name.

For a [canonical source](/adding-urls/#source-urls) page, the symbolic name
is always `'source'`.


## Using other data sources

Sometimes you might want to refer to another data source within a template.
You can use the `lookup()` function to return the data for any named source,
like so:

```html
{% with post=lookup("something-amazing") %}
<p>
  If you're bored, why not read our most popular post
  <a href='{{post.path}}'>{{post.title}}</a>?
</p>
{% endwith %}
```
