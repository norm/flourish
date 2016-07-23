# Template variables

Every generator makes some variables available to templates. They are
documented for each individual [generator](/api-flourish-generators).

## Adding more — the site configuration

If you want to add more variables you can use in your templates, you can add
new key/value pairs to the [site configuration file](/site-configuration/)
file. They are made available to templates as `{{site.key}}`.

## Adding more — the global context

If you need to add variables that are dependent on code, not just hard-coded
strings, you can add global context to your templates.

In `generate.py`, add something like the following:

```python
def work_out_code_stuff():
    return "Some code %s." % 'stuff'

def list_of_stuff():
    stuff = []
    for i in range(1, 3):
        stuff.append("Stuff part %s" % i)
    return stuff

def global_context(self):
    return {
        'code_stuff': work_out_code_stuff(),
        'stuff_list': list_of_stuff(),
    }

GLOBAL_CONTEXT = global_context
```

Then in your templates you could use the values like so:

```html
<p>{{global.code_stuff}}</p>

<ul>
  {% for stuff in global.stuff_list %}
    <li>{{stuff}}</li>
  {% endfor %}
</ul>
```
