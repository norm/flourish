# Flourish API: `flourish.generators.atom.CSVGenerator`

`CSVGenerator` is the class for generating a CSV file based on sources.

Other than as noted below, it behaves the same as
[`BaseGenerator`](/api-flourish-generators-base/).

```python
from flourish.generators import csv

PATHS = (
    ...
    csv.CSVGenerator(
        name = 'csv-file',
        path = '/index.csv',
    ),
    ...
)

```


## Class attributes

  * `fields` — The source fields to include in the CSV file. Default
    is `['title', 'published']`.
  * `order_by` — This generator should sort matching sources in this way.
    Default value is `-published` (most-recent first).
  * `sources_exclude` — This generator should exclude sources that match
    this filter. Default value is `None`.
  * `sources_filter` — This generator should only use sources that match
    this filter; see
    [Filtering down to specific sources](/api-flourish/#filtering-down-to-specific-sources).
    Default value is `None`.


## Methods

### output_to_file()

Generates the CSV file by looping over the source objects and calling 
`get_row` to build the CSV.

Bypasses `render_output` entirely.

### get_fields()

Returns a list of fields that should be included in the CSV. Override
this method if you need more control than setting the `fields` class
attribute.

### get_row(object)

Returns a dictionary of fields and their values. Override this method
if you need to more than look up the values from the source object.

### get_field_value(object, field)

Returns the value of the field in the source object. By default will turn
a list of strings (eg tags) into a colon-delimited string. Override this
method if you need to alter values from the source object.

### render_output()

Not called.

### get_context_data()

Not called.

### get_template()

Not called.

### get_template_name()

Not called.

### render_template(template, context_data)

Not called.
