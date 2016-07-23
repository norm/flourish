# Flourish API: `flourish.generators.IndexGenerator`

`IndexGenerator` is the class for generating pages that contain lists of
sources. For example: a list of links such as an archive page, or an
aggregated page such as a one-page summary.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).


## Class attributes

  * `sources_filter` — This generator should only use sources that match
    this filter; see
    [Filtering down to specific sources](/api-flourish/#filtering-down-to-specific-sources).
    Default value is `None`.
  * `sources_exclude` — This generator should exclude sources that match
    this filter. Default value is `None`.
  * `order_by` — This generator should sort matching sources in this way.
    Default value is `None`.
  * `template_name` — This generator should use this template when rendering
    the content. Default value is `index.html`.


## Context variables

  * `current_url` — the URL of this page
  * `objects` — a list of all matching source objects for the current URL
  * `pages` — a list of all matching source objects for the current URL
  * `site` — a dictionary containing all of the keys in the `_site.toml`
    configuration file

## Mixins

`IndexGenerator` includes the features of
[`PageIndexContextMixin`](/api-flourish-generators/#pageindexcontextmixin).

