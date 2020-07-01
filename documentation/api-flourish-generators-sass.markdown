# SassGenerator

`SassGenerator` is the class for generating CSS files from SASS-formatted
sources.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).


## Class attributes

  * `output_dir` — This generator will output generated CSS files within
    this directory in the generated site. Default value is `css`.
  * `output_style` — This generator will use this output style from Sass.
    Default value is `expanded`. Other values are `nested`, `compact`, and
    `compressed`.


## Methods

### get_url_tokens

Returns the pathnames to all non-partial `.scss` files within the configured
`sass_dir` in Flourish.

### get_current_url(tokens)

Returns the pathname of an individual CSS file to be generated.

### get_objects(tokens)

Overrides the default to return nothing, as Source objects do not apply.

### render_output()

Bypasses 

Bypasses `get_context_data`, `get_template`, `get_template_name` and
`render_template`, as they do not apply. Directly compiles the source
Sass into CSS and returns that.

### render_output()

 instead constructing the Atom feed programmatically
using the `AtomFeed` class provided by [pyatom].

[pyatom]: https://pypi.python.org/pypi/pyatom

### get_context_data()

Not called.

### get_template()

Not called.

### get_template_name()

Not called.

### render_template(template, context_data)

Not called.
