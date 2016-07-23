[TOC]

# Adding URLs to your Flourish site

Once you have [added some sources](/adding-sources/) and [created the
generate.py script](/generating-output/), you need to add URLs.


To generate webpages for the sources you add you will need code like this in
your `generate.py`:

```python
URLS = (
    (
        '/',
        'homepage',
        IndexGenerator.as_generator()
    ),
    (
        '/tags/#tag',
        'tags-tag',
        IndexGenerator.as_generator()
    ),
    ...
)
```

In between the brackets are three arguments. The first is the URL path,
explained below; the second is a symbolic name to represent this type of page,
the third is what code should be run to create each page, explained in
[Generating the HTML](/generating-html/).


## URL paths

The path is where in the site the page(s) are generated. 

A hash (`#`) in the path of a URL represents a replaceable token, that will be
substituted as the output is generated. The alphanumerics that follow the hash
represent the key to use (as found in source TOML). 

### Automatic token

The following token is automatically available without you having to add
it explicitly to your sources:

  * `slug` — always comes from the filename of the source TOML or
    Markdown file

### Multiple pages from single tokens

If a URL has a token with more than one possible subtitution, then multiple
pages are generated. In the above sample, the 'tags-tag' page has the URL
`/tags/#tag`. One page would be generated for each tag key listed across the
sources of the site.
