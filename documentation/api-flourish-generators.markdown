[TOC]

# Flourish API: `flourish.generators`

The generators in Flourish are responsible for turning one or more source
objects into output HTML.

## Subclassing the generators

If you need to alter the way a page or pages are being generated, it should
normally be possible to subclass one of the default generators and modify
only a small part of it.

## The included generators

  * [`BaseGenerator`](/api-flourish-generators-base/) — the base class of all
    Flourish generators
  * [`PageGenerator`](/api-flourish-generators-page/) — the class for
    generating individual source pages
  * [`IndexGenerator`](/api-flourish-generators-index/) — the class for
    generating lists of source pages
  * [`AtomGenerator`](/api-flourish-generators-atom/) — the class for
    generating an Atom feed

## The included mixins

### PageContextMixin

Adds the first of `self.source_objects` to the template context as `page` as
well as all key values from that object. For example, a TOML source of:

```python
title = 'About this site'
tag = ['about', 'information']
noindex = true
```

would make all of `{{page}}`, `{{title}}`, `{{tags}}`, and `{{noindex}}`
values available for use in templates.

### PageIndexContextMixin

Adds the list of source objects to the template context as `pages`.
