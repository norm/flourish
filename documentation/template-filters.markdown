# Template filters

In addition to the template filters provided by [Jinja][jf],
you can add your own in your `generate.py`:

```python
def add_cliche(var):
    return var + 'I am a cliche that lives next door.'

TEMPLATE_FILTERS = {
    'cliche': add_cliche,
}
```

`TEMPLATE_FILTERS` is a dict that maps the filter name as it will appear
in the templates to a callable.

[jf]: https://jinja.palletsprojects.com/en/2.11.x/templates/#filters

## Built-in

Flourish comes with two filters that you can use:

```python
from flourish.filters import ordinal

TEMPLATE_FILTERS = {
    'ordinal': ordinal,
}
```

* `ordinal`

    Given an integer, will return the ordinal suffix of that number
    in English, ie. `st`, `nd`, `rd`, or `th`.

    ```html
    {{page.published.day}}{{page.published.day|ordinal}}
    ```

* `month_name`

    Given an integer between 1 and 12, returns the name of that month.

    ```html
    <h1>Articles for {{month|month_name}}</h1>
    ```
