[TOC]

# Adding paths to your Flourish site

Once you have [added some sources](/adding-sources/) and [created the
generate.py script](/generating-output/), you need to add paths in order
to create any HTML.

In your `generate.py`, you will need a list of generators:

```python
PATHS = (
    SourceGenerator(
        name = 'source',
        path = '/#slug',
    ),
    ...
)
```

Each generator has two mandatory arguments, `name` and `path`, and will
produce all possible variations of a given path.


## `name`

The `name` argument to a generator is a unique symbolic representation of
what this generator produces. For example, `homepage` or `year-index`. 
The name is most commonly used in the
[`path()` template function](/template-functions/#resolving-paths)
for producing paths without hard-coding them. With the exception of the
special case name `source`, they have no other meaning.

### The special name `source`

One name is treated slightly differently. If you declare a name of `source`
on a generator, it is treated by Flourish to represent the canonical path
of every source. When you get the link to a source using the `source.url`
method, it will use this path, even if other generators will also create
pages from that source.


## `path`

The path is where in the site the page(s) are generated.

A hash (`#`) in the path represents a replaceable token that will be
substituted as the output is generated. The alphanumerics that follow the hash
represent the key to use (as found in source TOML).

### Automatic tokens

The following tokens are automatically available without you having to add
them explicitly to your sources:

  * `slug` — always comes from the filename of the source TOML, JSON, or
    Markdown file (explained further in 
    [Adding Sources](/adding-sources/#the-slug))
  * `year`, `month`, `day` — are created from the `published` key, if it
    is a timestamp (explained further in [Adding sources](/adding-sources/))
    # FIXME better link

In the example above, the path was `/#slug`. This means each source will be
generated at a path that matches the slug of the source. For example, a source
file `photos/grand-canyon.toml` has the slug `photos/grand-canyon`, so the
path would be `/photos/grand-canyon`. Note the absence of `/` at the start of
the slug, which is why the path adds it explicitly.

### Multiple tokens in a path

Using the slug is the most common pattern for creating output from sources,
but you are not restricted to only this. Some blogs commonly have posts that
indicate the date of publication, this can be done by using a path such as
`/#year/#month/#slug`. Your source doesn't have to be located within a
year/month directory structure, instead that comes from the `published`
timestamp.

For example, if the `photos/grand-canyon.toml` contained this `published`
timestamp:

```python
published = 2016-02-14T13:56:22Z
```

then the generated path would be `/2016/02/photos/grand-canyon`.

### Multiple pages from single tokens

If a path has a token with more than one possible subtitution, then multiple
pages are generated. For example, for a source URL path of
`/#year/#month/#slug` all three tokens only have one value, so only one page
would be generated. However, if you had a source file `example-page.toml`,
containing these keys:

```python
title = 'Example page'
tag = ['sample', 'introduction']
```

then the source URL path `/#tag/#slug` would generate two pages:

  * `/sample/example-page`
  * `/introduction/example-page`

This is more commonly used for index pages (eg `/archives/#year`,
`/tags/#tag`) than it is for sources, which usually only have the one,
canonical, path.


## `extras`

FIXME [template's context][] link?
Extra values to be passed to the template's context.
