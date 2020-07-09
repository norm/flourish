# Flourish API: `flourish.generators.sass.SassGenerator`

`SassGenerator` is the class for generating CSS files from SASS-formatted
sources.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).

```python
from flourish.generators import sass

PATHS = (
    ...
    sass.SassGenerator(
        name = 'stylesheet',
        path = '/css/#sass_source.css',
    ),
    ...
)
```


## Path token

The path token **must** be `sass_source`.


## Class attributes

  * `output_style` — This generator will use this output style from Sass.
    Default value is `expanded`. Other values are `nested`, `compact`, and
    `compressed`.


## Methods

### get_path_tokens

Returns the pathnames to all non-partial `.scss` files within the configured
`sass_dir` in Flourish.

### get_objects(tokens)

Overrides the default to return nothing, as Source objects do not apply.

### render_output()

Bypasses `get_context_data`, `get_template`, `get_template_name` and
`render_template`, as they do not apply. Directly compiles the source
Sass into CSS and returns that.

### get_context_data()

Not called.

### get_template()

Not called.

### get_template_name()

Not called.

### render_template(template, context_data)

Not called.
