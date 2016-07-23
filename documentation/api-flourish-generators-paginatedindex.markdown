# Flourish API: `flourish.generators.PaginatedIndexGenerator`

`PaginatedIndexGenerator` is the class for generating paginated pages that
contain lists of sources. For example: a series of list of links such as site
archives.

Other than as noted below, it behaves the same as
[`IndexGenerator`](/api-flourish-generators-index/).


## Class attributes

  * `per_page` — the number of source objects in each paginated page;
     the default value is `10`
  * `order_by` — this generator should sort matching sources in this way
  * `sources_filter` — this generator should only use sources that match
    this filter; see
    [Filtering down to specific sources](/api-flourish/#filtering-down-to-specific-sources)
  * `template_name` — the template to use to render this page; the default
    value is `index.html`

## Template context variables

  * `current_page` — the [`Page`](/api-flourish-paginator/#page) instance
    for this single page within the set of pages
  * `current_url` — the URL of this page
  * `objects` — a list of all matching source objects for the current URL
  * `pages` — a list of all matching source objects for the current URL
  * `pagination` — the [`Paginator`](/api-flourish-paginator/) instance for
    this set of pages
  * `site` — a dictionary containing all of the keys in the `_site.toml`
    configuration file

## Generator method flow

`PaginatedIndexGenerator` modifies the usual generator method flow as 
follows:

  * [`generate`](#generate) calls:
      * [`get_url_tokens`](#get_url_tokens), then for every set of tokens found:
          * [`get_current_url`](#get_current_urltokens)
          * [`get_paginated_objects`](#get_paginated_objects), which calls:
              * [`get_objects`](#get_objectstokens), which calls:
                  * [`get_filtered_sources`](#get_filtered_sources)
                  * [`get_order_by`](#get_order_by)
              * [`get_per_page`](#get_per_page)
          * then for every page returned by `get_paginated_objects`:
              * [`output_to_file`](#output_to_file), which calls:
                  * [`get_output_filename`](#get_output_filename)
                  * [`render_output`](#render_output), which calls:
                      * [`get_context_data`](#get_context_data)
                      * [`get_template`](#get_template), which calls:
                          * [`get_template_name`](#get_template_name)
                      * [`render_template`](#render_templatetemplate-context_data)

## Methods

### generate()

Finds the matching [URL tokens](#get-url-tokens) for the URL, and for each set
determines the URL (and hence, where to write the output page to), fetches the
matching source objects, paginates them, and for every page outputs what is
generated to a file.

### get_paginated_objects(tokens, base_url)

Fetches the list of source objects that match the current URL tokens, after
having already fetched the filtered sources — ie. the results of calling
`filtered_sources.filter(**tokens)` — and then paginates them, returning
a [`Paginator`](/api-flourish-paginator/) object.

### get_per_page()

Returns the number of source objects to have on each page.

### get_context_data()

Adds `current_page` and `pagination` to the template context data.
