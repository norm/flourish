# Including the range of years of your content

If you need to use the range of years in which content was created, first
ensure that anything you want to count is using the
[special key](/adding-sources/#special-keys-in-sources) `published` to store
the date (it is fine to duplicate the date if you are already using a
different key).

Add the following to your `generate.py`:

```python
from flourish import helpers

def global_context(self):
    return {
        'publication_range': helpers.publication_range(self.flourish),
    }

GLOBAL_CONTEXT = global_context
```

This makes a variable `global.publication_range` available to all of your
templates, which contains a string much like "2012–2016".

You can use this in your templates like so:

```html
<footer>
  <p>Copyright {{global.publication_range}} {{site.author}}.</p>
</footer>
```
