# The site configuration file

A file called `_site.toml` must exist in the source directory, and has to
contain at least the following three keys:

```toml
author = ''
base_url = ''
title = ''
```

Although these are required, they can be left blank if you are not
generating Atom feeds.

Values for author, title, and the base URL of the published site are
required to generate valid Atom feeds.


## Optional keys

There are other keys that Flourish will treat as having special meaning.

  * `future`

    ```toml
    future = false
    ```

    If `future` is set to `false`, any source that has a `publication` date
    that is in the future at the point the site is generated will be ignored.

    By default future publications are included.

  * `bucket`

    ```toml
    bucket = 'some.bucket'
    ```

    When using `flourish upload` to push changes to an Amazon S3 bucket,
    this setting tells Flourish what bucket to use.


## Using in templates

The values in the file are made available to all templates under the `site`
key. For example, a site's footer could include:

```html
<footer>
  <p>Copyright {{global.copyright_year_range}} {{site.author}}.</p>
</footer>
```
