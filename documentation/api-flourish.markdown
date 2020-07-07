[TOC]

# Flourish API: `flourish`

To create a Flourish instance:

```python
from flourish import Flourish

# assume default named directories located in current working directory
fl = Flourish()

# differently named directories
fl = Flourish(
    source_dir='words',
    templates_dir='html',
    output_dir='site',
    sass_dir='styles',
)
```


## Finding sources

```python
# get a SourceList object
sources = fl.sources

# get all sources
for source in fl.sources.all():
    print(source)

# get sources published before 2016
for source in fl.sources.filter(published__lte=date(2016, 1, 1))
    ...
```

`flourish.sources` will return a [`SourceList`](/api-flourish-sourcelist/)
object, which can be used to query the sources in a number of ways.


## Adding paths

### Source URLs

```python
fl.canonical_source_url('/#slug', code_ref)
```

Adds the URL for all sources. The parameters are:

 1. the URL path, including the token
    (see [URL paths](/adding-urls/#url-paths))
 2. the code that will generate these pages
    (see [Generating the HTML](/generating-html/))

### Other URLs

```python
fl.add_url('/tags/#tag', 'tag-page', code_ref)
```

Adds a URL. The parameters are: the URL path, including the token

 1. the URL path, including the token
    (see [URL paths](/adding-urls/#url-paths))
 2. a string as a symbolic name for this URL
    (see [Finding URLs](#finding-urls))
 3. the code that will generate these pages 
    (see [Generating the HTML](/generating-html/))


## Finding URLs

### Resolving a single URL

```python
fl.resolve_url('homepage')
fl.resolve_url('source', slug='about/flourish')
fl.resolve_url('month-page', year=2012, month=6)
```

Return the URL for a given symbolic name. If the URL contains tokens (see
[URL paths](/adding-urls/#url-paths)) they need to be passed as arguments,
or the URL will not resolve.


### Resolving many URLs

```python
fl.all_valid_filters_for_url('source')
```

Returns a list of all of the valid arguments (as key/value pairs) for a given
symbolic name. Each item in the list can be passed to `resolve_url()` to 
get a URL.


## Generating the website

```python
fl.generate_url('homepage', report=True)
```

Generate the named URL. The optional argument `report` will make Flourish list
each generated output file when it is set to `True`.

```python
fl.copy_assets(report=False)
```

Copy all [assets](/adding-assets/) to the output directory. The optional
argument `report` will make Flourish list each asset file copied when it
is set to `True`.


```python
fl.generate_site(report=True)
```

This first wipes the output directory, then generates every URL that Flourish
knows about, then copies over all [assets](/adding-assets/) from the source
directory.
