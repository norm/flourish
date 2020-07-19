[TOC]

# Release notes for Flourish

## 0.8 - UNRELEASED

  * Always apply the MIME type of a file when uploading to S3.
  * Speed up previewing a site with dynamic generation by only re-reading
    source files that have changed, instead of everything each time.
  * Add a [generator for compiling SASS][sass] into CSS.
  * Add [generators][cal] for calendar-based index pages.
  * Altered the result of `flourish.sources` to be a [`SourceList`][sl]
    object rather than a `Flourish` object.
  * A substantial and breaking change to how generators are declared in the
    `generate.py` file. Previously, Flourish used `URLS` and `SOURCE_URL`, but
    now only uses `PATHS`, and how generators are declared has changed. See
    the documentation on [adding paths][ap].
  * Set Atom feeds to include at most 20 items by default.
  * Bug fixes and performance improvements.

[sass]: https://flourish.readthedocs.io/en/latest/api-flourish-generators-sass/
[cal]: https://flourish.readthedocs.io/en/latest/api-flourish-generators-calendar/
[sl]: https://flourish.readthedocs.io/en/latest/api-flourish-sourcelist/
[ap]: https://flourish.readthedocs.io/en/latest/adding-paths/


## 0.7 — 16 June 2020

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

[gn]: https://flourish.readthedocs.io/en/latest/generating-the-site/
[ft]: https://flourish.readthedocs.io/en/latest/template-filters/
[fn]: https://flourish.readthedocs.io/en/latest/template-functions/
[ln]: https://flourish.readthedocs.io/en/latest/linking-sources/
[as]: https://flourish.readthedocs.io/en/latest/adding-sources/


## 0.6 — 6 August 2016

  * Changed how assets are treated. Previously they were kept in their own
    directory, now they are taken from the same `source` directory as the
    source files, `generate.py` and `_site.toml`.


## 0.5

This release and all before it are from before release notes were being kept.
