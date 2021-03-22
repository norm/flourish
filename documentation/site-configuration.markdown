# The site configuration file

The file called `_site.toml` in the source directory can be used to set
configuration parameters used by Flourish's code and in templates.
It is not a requirement unless you are using a generator that needs
specific keys set.


## Required by generators

  * `AtomGenerator`

        ```toml
        author = 'Wendy Testaburger'
        base_url = 'http://wendytestaburger.com'
        title = 'Wendyblog'
        ```

    In order to generate valid Atom feeds, the
    [`AtomGenerator`](/api-flourish-generators-atom/) needs three values:

      * `author` is used in the `<author>` element at the root of the
        Atom feed, and is used as the default author name for each
        entry (but can be overridden)
      * `base_url` is prepended to the paths of entries in the Atom
        feed
      * `title` is used in the `<title>` element at the root of the
        Atom feed.


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

  * `cloudfront_id`

    ```toml
    cloudfront_id = 'E3ZZZZSOMETHING'
    ```

    When using `flourish upload --invalidate` to push changes to an Amazon
    S3 bucket that is behind a CloudFront distribution, this setting
    tells Flourish what the distribution ID is.

## Using in templates

The values in the file are made available to all templates under the `site`
key. For example, a site's footer could include:

```html
<footer>
  <p>Copyright {{global.copyright_year_range}} {{site.author}}.</p>
</footer>
```
