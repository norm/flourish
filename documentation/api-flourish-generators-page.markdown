# Flourish API: `flourish.generators.PageGenerator`

`PageGenerator` is the class for generating individual source pages.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).


## Class attributes

  * `template_name` is set to `page.html`

## Context variables

  * `current_url` — the URL of this page
  * `objects` — a list of all matching source objects for the current URL
  * `page` — the source object matching the current URL
  * `site` — a dictionary containing all of the keys in the `_site.toml`
    configuration file
  * `...` — every key that has been set in the matching source object

## Mixins

`PageGenerator` includes the features of
[`PageContextMixin`](/api-flourish-generators/#pagecontextmixin).

## Generator method flow

### get_template_name()

This method is altered to returns the value of `template_name` **unless** the
page source has set the key `type`, in which case it returns the value of
`type` with ".html" appended, or if the key `template` has been set, when that
value is returned unaltered.

For example, the following TOML would give a template name of `photo.html`:

```python
title = 'Grand Canyon'
type = 'photo'
...
```

whereas this would give a template name of `broken`:

```python
title = 'Grand Canyon'
type = 'photo'
template = 'broken'
...
```
