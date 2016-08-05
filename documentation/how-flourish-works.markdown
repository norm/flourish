# How Flourish works

Flourish generates websites by passing content ("source") through templates
to create pages that you define (rather than only those provided in the code,
or by adding a plugin).

In order to create a website with Flourish, you will need three directories:

  * `source` — contains the [sources of the pages](/adding-sources/),
    the [site configuration](/site-configuration/), the
    [generation script](/generating-the-site), and any 
    [assets](/adding-assets/) for the site
  * `templates` — contains the wrapper HTML used to convert the sources into 
    webpages
  * `output` — contains the generated website

You can use the `flourish` command-line script to:

  * setup a new example website
  * preview the website locally, as you work on it
  * generate the website, ready to upload to your hosting provider
  * upload the website to Amazon S3 (if you are using S3 to host the website,
    or just to keep a backup of your site)
