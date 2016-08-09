[TOC]

# Adding sources to Flourish

Flourish uses source files to contain the content of site to be generated.

Three types of source file are supported, and they can be mixed and matched
at will:

* [TOML][toml]
* [JSON][json]
* [Markdown][md]

All sources are treated as though they contain UTF-8 content. If they contain
characters of a different character set, you will have problems. Modern text
editors save files in UTF-8 by default.


## The slug

The filename and subdirectory/-ies of the source file determines the default
URL that piece of content will have in the site, also known as the "slug". The
filename (slug) can only contain letters, numbers, hyphens (`-`) and
underscores (`_`). It cannot contain other punctuation characters, such as
periods (`.`) or quotation marks (`'"`).

* Correct filenames:
    * `about-me.toml`
    * `2016/06/02/valentines-day.markdown`
* Incorrect filenames:
    * `about.me.toml`
    * `2016/06/02/valentine's-day.markdown`

**Note**: a slug that ends `/index`  will be trimmed to ending `/` when
treated as a URL. For example, a source file `more/about/index.toml` will have
the slug `more/about/index` and the URL `more/about/` when rendered.

## Source data

A source is a set of keys and values. These specify aspects of a web page,
such as the title, content, when it was created, and anything else you might
need. 

### Example TOML source

```python
# example TOML file

body_markdown = """
# Example blog post

I am a blog post, written in Markdown.
"""

published = 2016-07-01T12:00:00Z
tag = ['example', 'toml']
title = 'A TOML example'
type = 'post'
```

For more information on the rules of correctly formatting TOML sources, see
the [TOML specification][tomlspec].

The first thing to note from this example is the key `body_markdown`. Flourish
will automatically process Markdown content in any key that ends `_markdown`
and make the resulting HTML available as that key minus the `_markdown`. So in
this example `body` would contain HTML (also see "Adding Markdown to sources"
below).

Second, the key `published` contains a timestamp. This is in a specific 
format, called [ISO 8601][iso]. Although this format supports more 
variation, Flourish currently only understands timestamps in the format 
`YYYY-MM-DDTHH:MM:SSZ` (the year, a hyphen, the month as two digits, a hyphen,
the day of the month as two digits, a hyphen, the letter `T`, the hours
of the day expressed as a 24-hour clock, the minutes, and the seconds, and
lastly the letter `Z`). This expresses the time as being in [UTC][utc] 
(or Greenwich Mean Time). Better support for dates and times outside of UTC
will come in a later version.


### Example Markdown source

```markdown
---
published = 2016-07-01T12:00:00Z
tag = ['example', 'markdown']
title = 'A Markdown example'
---

# Another example blog post

I am a blog post, also written in Markdown.
```

Note that this example demonstrates that you can embed TOML in the Markdown
file by putting it at the very top of the file and surrounding it with triple
hyphens on a line by themselves. The TOML can also be surrounded by triple
backticks (\`\`\`).

The content of the file (without the embedded TOML) is put into the key
`body_markdown` (identical to the Markdown in the TOML in the first example).

This technique of including metadata in a Markdown file is called
"front matter". Note that it is entirely optional, and a source can contain
just Markdown without any front matter.

## Adding Markdown to sources

In addition to putting the Markdown in the source as shown in the examples
above, there is a second way to add Markdown content — by using associated
filenames.

Any source can have other Markdown content added from separate files,
providing that they share the slug part of the filename. For example, a
source with the filename `blog-post.toml`, will automatically contain the
content of the file `blog-post.body.markdown` as though it had been in
the key `body_markdown` in the TOML.

The advantage of having separate files for the Markdown is readability — both
the original source file and the Markdown are more easily understood when
looking at them as separate entities.

The disadvantage is having to deal with more files, and it not being
immediately obvious when looking at a source file that it may have more
keys that are currently shown.


## Adding HTML to sources

In the same manner as adding Markdown shown above, raw HTML can be added.
For example, a source with the filename `blog-post.toml` will automatically
contain the content of the file `blog-post.body.html` as though it had been
in the key `body` in the TOML.


## Special keys in sources

You are free to use any keys for any purpose in your Flourish source
documents, but the following keys have special treatment you should
be aware of:

  * `author` — is used to mark the author of a source when
    generating Atom feeds (this overrides the author set in
    the [site configuration](/site-configuration/) for that source only).
  * `body` — is used as the content of an individual source when generating
    Atom feeds.
  * `published` — is used as the publication timestamp of a source when
    generating Atom feeds, and is used as the basis of the `#year`, `#month`
    and `#day` special tokens in [URLs](/adding-urls/). It is expected to be a
    timestamp (explained in [Adding sources](/adding-sources/)).
  * `title` — is used as the title of an individual source when generating
    Atom feeds.
  * `updated` — is used as the "last updated" timestamp of a source when
    generating Atom feeds. It is expected to be a timestamp (explained in
    [Adding sources](/adding-sources/)).
  * `..._fkey` — anything ending `_fkey` is assumed to be part of a foreign
    key lookup. See the advanced topic
    [Linking sources together](/linking-sources/).
  * `..._set` — anything ending `_set` is assumed to be part of a reverse
    foreign key lookup. See the advanced topic
    [Linking sources together](/linking-sources/).


[iso]: https://en.wikipedia.org/wiki/ISO_8601
[json]: http://json.org
[md]: http://daringfireball.net/projects/markdown/
[toml]: https://github.com/toml-lang/toml
[tomlspec]: https://github.com/toml-lang/toml#user-content-spec
[utc]: https://en.wikipedia.org/wiki/Coordinated_Universal_Time
