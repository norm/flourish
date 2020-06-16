[TOC]

# Release notes for Flourish

## 0.7 — UNRELEASED

  * Flourish can now [generate specific paths][gn] as well as the entire site.
    The `preview` command-line option now takes advantage of this to only
    regenerate pages as they are requested (important for large sites, as full
    site generation can take minutes).
  * How Flourish uses its command-line options has changed slightly. Run
    `flourish --help` to find out more.
  * Make [filters available for templates][ft]. Two built-ins are provided —
    `month_date` to return the name of a given month by number, and `ordinal`
    to provide an English ordinal suffix to numbers (eg `3rd`).
  * Make two [functions available in templates][fn] — `url` to get URLs,
    `lookup` to fetch source data.
  * Provide ways of [linking sources together][ln].
  * Markdown [front matter][as] can now also be surrounded by backticks
    (`` ``` ``) in addition to the default hyphens (`---`), in order for them
    to render better in some Markdown previews (eg GitHub).
  * Alters the code to work under python 3.x, dropping support for python 2.
    Tests are run by GitHub for versions 3.5 through 3.8.

  * Some generation bugs have been fixed.

[gn]: http://flourish.readthedocs.io/en/latest/generating-the-site/
[ft]: http://flourish.readthedocs.io/en/latest/template-filters/
[fn]: http://flourish.readthedocs.io/en/latest/template-functions/
[ln]: http://flourish.readthedocs.io/en/latest/linking-sources/
[as]: http://flourish.readthedocs.io/en/latest/adding-sources/


## 0.6 — 6 August 2016

  * Changed how assets are treated. Previously they were kept in their own
    directory, now they are taken from the same `source` directory as the
    source files, `generate.py` and `_site.toml`.


## 0.5

This release and all before it are from before release notes were being kept.
