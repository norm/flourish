[TOC]

# Flourish API: `flourish.generators.base.BaseGenerator`

`BaseGenerator` contains the majority of Flourish's page generation code, and
should be easily subclassable where code needs to alter the default manner
of generating pages.

## Class attributes

  * `limit` — This generator should return no more than `limit` sources.
  * `order_by` — This generator should sort matching sources in this way.
    Default value is `None`.
  * `sources_exclude` — This generator should exclude sources that match
    this filter. Default value is `None`.
  * `sources_filter` — This generator should only use sources that match
    this filter; see
    [Filtering down to specific sources](/api-flourish/#filtering-down-to-specific-sources).
    Default value is `None`.
  * `template_name` — This generator should use this template when rendering
    the content. Default value is `None`.

## Context variables

  * `current_url` — the URL of this page
  * `objects` — a list of all matching source objects for the current URL
  * `site` — a dictionary containing all of the keys in the `_site.toml`
    configuration file

## Generator method flow

When the generator is instantiated from `generate.py`, `setup()` is called
and Flourish passes itself in as an argument so the generator can store
the reference for later use.

When page generation starts, Flourish calls `generate()`, which causes the
following things to be run in order:

  * [`generate`](#generate) calls:
      * [`get_url_tokens`](#get_url_tokens) if tokens were not passed as an
        argument; then for every set of tokens:
          * [`generate_path`](#generate_pathtokens), which calls:
              * [`get_current_url`](#get_current_urltokens)
              * [`get_objects`](#get_objectstokens), which calls:
                  * [`get_filtered_sources`](#get_filtered_sources)
                  * [`get_order_by`](#get_order_by)
              * [`output_to_file`](#output_to_file), which calls:
                  * [`get_output_filename`](#get_output_filename)
                  * [`render_output`](#render_output), which calls:
                      * [`get_context_data`](#get_context_data)
                      * [`get_template`](#get_template), which calls:
                          * [`get_template_name`](#get_template_name)
                      * [`render_template`](#render_templatetemplate-context_data)

### generate()

Generate all possible pages for a given page type.

Unless given a subset of tokens to use, it fetches all matching
[URL tokens](#get-url-tokens) for the URL. For each set of tokens, call 
[`generate_path`](#generate-pathtokens) to generate a single page.

### get_url_tokens()

Checks the current URL against all sources to find the list of matching
tokens to substitute into the URL.

For example, with a single source document:

```toml
title = 'Blog Post'
tag = ['post', 'introduction']
```

and a URL of `/tags/#tag`, it would return a structure:

```python
[
    {'tag': 'introduction', },
    {'tag': 'post', },
]
```

### generate_path(tokens)

Calls [`get_current_url`](#get-current-urltokens) to determine the page
to be generated, [`get_objects`](#get-objects) to get the sources that
match the tokens, and [`output_to_file`](#output-to-file) to create the
page.

### get_current_url(tokens)

Works out the URL to be generated, based upon the URL tokens. 

To continue the above example, it would return `/tags/introduction` for the
first set of tokens, and `/tags/post` for the second.

### get_objects(tokens)

Returns the list of source objects that match the current URL tokens, after
having already fetched the filtered sources — ie. the results of calling
`filtered_sources.filter(**tokens)`.

### get_filtered_sources()

Returns all source objects that match the current filter applied by the view.

If the class has an attribute of `sources_filter`, then only source objects
matching this will be used as possible objects for the generator. See
[Filtering down to specific sources](/api-flourish/#filtering-down-to-specific-sources).

If `sources_filter` is not set, then all source objects will be used.

### get_order_by()

Returns the ordering for the source objects. See
[Ordering sources](/api-flourish/#ordering-sources).

### output_to_file()

Gets the filename to write the output to, and the output, and writes the file
(creating any subdirectories of the output directory as needed).

### get_output_filename()

Returns the filename to be used, based on the
[current URL](#get_current_urltokens).

For example, with a URL of `/tags/introduction`, this would return 
`/tags/introduction.html`.

### render_output()

Returns the output for this page by getting the data to be used in the
template's context, getting the template and rendering the template with the
context data.

### get_context_data()

Returns the data to be used in the template's context.

### get_template(context)

Returns the template to use to render the page. Raises a `MissingValue`
exception if `get_template_name()` returns no value.

### get_template_name()

Returns the name of the template to use to render the page, which is
unset in `BaseGenerator`.

### render_template(template, context_data)

Returns the rendered output of applying the context data to the template.

