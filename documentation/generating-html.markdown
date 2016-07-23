[TOC]

# Generating the HTML

Once you have [added some sources](/adding-sources/),
[created the generate.py script](/generating-the-site/), and
[added some URLs](/adding-urls/), you need to know how the HTML is generated.


## Source pages

The default declaration for generating each source to an individual output
page in a Flourish site is:

```python
SOURCE_URL = (
    '/#slug',
    PageGenerator.as_generator(),
)
```

In between the brackets are two arguments. The first is the URL path, 
explained in [Adding URLs](/adding-urls/); the second is what code should be 
run to create each page.

The code `PageGenerator.as_generator()` will pass all of the key/value pairs
defined in the source to a template, render the template, and use the result
to write to the output HTML page.

### Default source page template

By default, this code will expect to use a template called `page.html`. A 
short example of this template looks like:

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{title}}</title>
</head>
<body>
  {{body}}
</body>
</html>
```

The parts surrounded by double curly brackets (eg `{{title}}`) are 
substitutions that use the value from the source. For example, this template
used against this source:

```python
title = "Example page"
body = "<p>Hello world.</p>"
```

would create the following HTML:


```html
<!DOCTYPE html>
<html>
<head>
  <title>Example page</title>
</head>
<body>
  <p>Hello world.</p>
</body>
</html>
```

### Overriding the default template

If you need to use a different template from `page.html` to render a given
source, you can set one of two keys:

  * `type` — the template becomes the value of this key with `.html` added;
    for example a source with `type = 'photo'` in its configuration will try
    to use the template `photo.html`.
  * `template` — the template becomes the value of this key with no
    modification; for example `template = 'pages/awesome-page.html'`

If both keys are set, the value of `template` is used.


## Index pages

To create the pages that link to your sources, you would use a URL declaration
like:

```python
URLS = (
    (
        '/',
        'homepage',
        IndexGenerator.as_generator()
    ),
)
```

In between the brackets are three arguments. The first is the URL path,
explained in [Adding URLs](/adding-urls/); the second is a symbolic name to
represent this page; the third is what code should be run to create it.

The code `IndexGenerator.as_generator()` will pass a list of all matching
sources to a template, render the template, and use the result to write
to the output HTML page.

### Default index page template

By default, this code will expect to use a template called `index.html`. A 
short example of this template looks like:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Index of pages</title>
</head>
<body>
  <ul>
    {% for page in pages %}
      <li>
        <a href='{{page.url}}'>{{page.title}}</a>
      </li>
    {% endfor %}
  </ul>
</body>
</html>
```

In the template `pages` is the list of all matching sources. This template
loops over each source within that (each being set to the variable `page`),
and uses keys from the source to link to the source page.


## Variables available in templates

### PageGenerator

  * `page` — the current source
  * `<key>` — any configuration of the current source

Configuration such as the page title is available both as `page.title` and
as `title` to make templates easier to read and write.

### IndexGenerator

  * `pages` — all sources that match the index being generated

### Common variables

Both generators also provide the following variables:

  * `current_url` — the URL of this page
  * `site` — the contents of the [site configuration](/site-configuration/)
    (eg `site.title`, `site.author`)


## More about the template language

Flourish uses Jinja2 to render templates. You can learn a lot more about the
things you can do in your templates by reading the
[Jinja2 documentation](http://jinja.pocoo.org).
