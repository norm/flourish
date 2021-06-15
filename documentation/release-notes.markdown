[TOC]

# Release notes for Flourish

## NEW_VERSION - UNRELEASED

High level description, if applicable.

#### New

  * Permanent (301) redirects from an old slug to a new location can be kept
    in the `_site.toml`:

        [permanent_redirects]
        "/index.php" = "/"

    and in an individual source:

        previous_slug = ['/page']


#### Other changes

#### Bug fixes

  * Stop reusing previously generated files in the live preview.
  * Use backwards-compatible importlib_resources for older pythons, and
    test that part of the code.

#### Dependency updates


## 0.10.0 - 11 Jun 2021

Improvements to the blueprint (previously called "recipe") page.

#### New

  * Live preview adds a permanent icon in the top-right that can be used
    to toggle back and forth between rendered page and blueprint.
  * In the blueprint:
    * Edit/create/delete Sectile fragments directly in page.
    * List the full Sectile fragments search path.

#### Bug fixes

  * In the blueprint:
    * show all Sectile dimensions, not just the ones that are set
    * pretty print the context data


## 0.9.7 - 3 June 2021

#### New

  * Serve asset files (eg CSS, images, etc) from the source directory
    during live preview.
  * Raising `self.DoNotGenerate` in a generator will stop the current
    page from being generated, without causing any errors.

#### Other changes

  * Allow overriding an Atom feed's author and title values.

#### Bug fixes

  * Fix wildcard generation of URLs. Some patterns were not matching, for
    example `flourish generate /2021/?` was generating `/2021/index.html` but
    not `/2021/04/21/index.html`, or any source with a slug starting
    `/2021/...`.
  * Stop live preview caching sectile-generated templates, which invalidated
    the point of being able to live preview changes as they are made.
  * An Atom feed without entries will still generate now.


## 0.9.6 - 22 April 2021

#### Bug fixes

  * Months and days in date-based path segments are treated as
    2-character segments, so now 4th June 2016 is generated
    as `/2016/06/04` not `/2016/6/4`.


## 0.9.5 - 7 April 2021

#### New

  * Sources can now include CSV files, which contain multiple sources
    in one file.

#### Other changes

  * Timestamps in generated CSV files now match the expected input format.


## 0.9.4 - 22 March 2021

#### Bug fixes

  * Three keys were enforced to exist in the `_site.toml` configuration
    which were used by the [Atom generator][atom], even if no Atom feeds were
    going to be generated. These requirements have been moved to the
    Atom generator, and the `_site.toml` is now optional.
  * Made some runtime errors in the command-line just use the error string
    without a full stacktrace, as the stacktrace adds no useful information.


## 0.9.3 - 3 March 2021

#### New

  * Add `--invalidate` option to `flourish upload` that issues a CloudFront
    invalidation on the paths uploaded.


## 0.9.2 - 22 February 2021

### New

  * Add `exclude_future` filter to sources that will remove anything with
    a `published` date in the future
  * Add `future` setting to the `_site.toml` that, when set to true,
    removes anything with a `published` date in the future from appearing
    to any generator (easier than filtering future sources individually)
  * Add `--exclude-future` and `--include-future` arguments to the
    `flourish generate` command, that will override the setting in
    `_site.toml` if necessary.


## 0.9.1 - 18 September 2020

#### Bug fixes

  * Remove stray `print` statement.


## 0.9 - 18 September 2020

#### New

  * Add a [CSV generator][csv].

#### Changes

  * Update the [Atom generator][atom] to allow some values to be
    overridden from the default. Mostly to allow the body of the Atom
    entry to include more content than just the source's body.

[csv]: https://flourish.readthedocs.io/en/latest/api-flourish-generators-csv/
[atom]: https://flourish.readthedocs.io/en/latest/api-flourish-generators-atom/


## 0.8 - 2 August 2020

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
  * Can use [Sectile][sec] for template assembly. Experimental, so not yet
    supported or documented.
  * When previewing the site, you can add `?showrecipe` to the URL to see
    a "recipe" page detailing the template(s) and context used to generate
    the page.
  * Change the special behaviour applied to the key `type` to apply to the
    key `page_type` to be more explicit as to its meaning.
  * Add `--dry-run` option to `flourish upload` to list what would be
    uploaded without actually doing so.
  * Bug fixes and performance improvements.

[sass]: https://flourish.readthedocs.io/en/latest/api-flourish-generators-sass/
[cal]: https://flourish.readthedocs.io/en/latest/api-flourish-generators-calendar/
[sl]: https://flourish.readthedocs.io/en/latest/api-flourish-sourcelist/
[ap]: https://flourish.readthedocs.io/en/latest/adding-paths/
[sec]: https://pypi.org/project/sectile/


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
