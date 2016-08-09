[TOC]

# Release notes for Flourish

## as yet unreleased

  * Make two [functions available in templates][fn] — `url` to get URLs,
    `lookup` to fetch source data.
  * Provide ways of [linking sources together][ln].
  * Markdown [front matter][as] can now also be surrounded by backticks
    (`` ``` ``) in addition to the default hyphens (`---`), in order for them
    to render better in some Markdown previews (eg GitHub).

[fn]: http://flourish.readthedocs.io/en/latest/template-functions/
[ln]: http://flourish.readthedocs.io/en/latest/linking-sources/
[as]: http://flourish.readthedocs.io/en/latest/adding-sources/


## 0.6 — 6 August 2016

  * Changed how assets are treated. Previously they were kept in their own
    directory, now they are taken from the same `source` directory as the
    source files, `generate.py` and `_site.toml`.


## 0.5

This release and all before it are from before release notes were being kept.
