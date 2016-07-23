# Adding date-based navigation to your site

To add some form of date-based navigation to your site, first ensure that
anything you want to show up in the date-based navigation is using the
[special key](/adding-sources/#special-keys-in-sources) `published` to store
the date (it is fine to duplicate the date if you are already using a
different key).

Add the following to your `generate.py`:

```python
from flourish import helpers

def global_context(self):
    return {
        'dates': helpers.all_valid_dates(self.flourish),
    }

GLOBAL_CONTEXT = global_context
```

This makes a variable `global.dates` available to all of your templates, which
contains a structure that lists all years, months and days that have
associated source objects.

Then, to generate indexes for the date-based navigation, add the following to
your `generate.py`:

```python
URLS = (
    # your existing URLs should be here, don't remove them,
    # just add the two new URLs listed below:
    (
        '/#year/',
        'year-index',
        IndexGenerator.as_generator()
    ),
    (
        '/#year/#month',
        'month-index',
        IndexGenerator.as_generator()
    ),
)
```

This will generate pages for each year and month that you can link to in 
the navigation.

Lastly, add something like this to your templates:

```html
<nav>
  <ul>
    {% for year in global.dates %}
      <li>
        <a href='/{{year.year}}/'>{{year.year}}</a>:
        <ul>
          {% for month in year.months %}
            <li><a href='/{{year.year}}/{{month.month}}'>{{month.month}}</a></li>
          {% endfor %}
        </ul>
      </li>
    {% endfor %}
  </ul>
</nav>
```

This will create a nested list of links to the year and month index pages.

Adjusting the content and styling of the generated navigation and index pages
is left up to you. If you need to use a different template, you can subclass
the generator code like so:

```python
# specialise the index generator with a new template
class YearIndexGenerator(IndexGenerator):
    template_name = 'year-index.html'

# use that in the URLS
URLS = (
    # ... existing URLs
    (
        '/#year/',
        'year-index',
        YearIndexGenerator.as_generator()
    )
)
```
