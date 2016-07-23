# How Flourish works

Flourish generates websites by passing content ("source") through templates
to create pages that you define (rather than only those provided in the code,
or by adding a plugin).

In order to create a website with Flourish, you will need four directories:

  * `source` — contains the [sources of the pages](/adding-sources/),
    the [site configuration](/site-configuration/) and
    [generation script](/generating-the-site)
  * `templates` — contains the wrapper HTML used to convert the sources into 
    webpages
  * `assets` — contains any extra files for the site, such as images and CSS
  * `output` — contains the generated website

You can use the `flourish` command-line script to:

  * preview the website locally, as you work on it
  * generate the website, ready to upload to your hosting provider
  * upload the website to Amazon S3 (if you are using S3 to host the website,
    or just to keep a backup of your site)
