# Flourish API: `flourish.generators.IndexGenerator`

`IndexGenerator` is the class for generating pages that contain lists of
sources. For example: a list of links such as an archive page, or an
aggregated page such as a one-page summary.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).


## Class attributes

  * `template_name` is set to `index.html`

## Context variables

  * `objects` — a list of all matching source objects for the current URL
  * `pages` — a list of all matching source objects for the current URL

## Mixins

`IndexGenerator` includes the features of
[`PageIndexContextMixin`](/api-flourish-generators/#pageindexcontextmixin).

