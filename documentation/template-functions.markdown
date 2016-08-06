# Template functions

There are functions made available for use in templates.


## Resolving URLs

If you hardcode URLs in links in your templates, you are forcing yourself to
edit multiple files if/when you change the URL. Rather than hardcoding URLs in
your templates you can use the `url()` function, like so:

```html
<nav>
  <ul>
    <li><a href='{{ url("homepage") }}'>Homepage</a></li>
    <li><a href='{{ url("tag-index", tag="css") }}'>Pages tagged CSS</a></li>
  </ul>
</nav>
```

The first argument is the [symbolic name of the URL](/adding-urls/) as defined
in your `URLS` list. If the URL requires any 
[replacable tokens](/adding-urls/#url-paths) those come after the name.

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
  <a href='{{post.url}}'>{{post.title}}</a>?
</p>
{% endwith %}
```
