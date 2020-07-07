# Adding date-based navigation to your site

The following will generate pages of the form:

* `/2020/index.html`
* `/2020/01/index.html`
* `/2020/02/index.html`
* ...

that contain links to individual source pages.


## Add the published date your sources

To add date-based navigation to your site, first ensure that anything
you want to show up in the date-based navigation is using the
[special key](/adding-sources/#special-keys-in-sources) `published` to store
the date (it is fine to duplicate the date if you are already using a
different key).


## Add year and month based index pages

To generate a year and month index pages, add the following to your
`generate.py`:

```python
from flourish.generators.calendar import (
    CalendarYearGenerator,
    CalendarMonthGenerator,
)

PATHS = (
    # ...
    # your existing paths should be here, don't remove them,
    # ...
    CalendarYearGenerator(
        path = '/#year/',
        name = 'year-index',
    ),
    CalendarMonthGenerator(
        path = '/#year/#month/',
        name = 'month-index',
    ),
)
```

Create a `calendar_year.html` template:

```html
<h1>Entries for {{year.year}}</h1>

<ol>
  {% for month in publication_dates %}
    {% with m=month.month %}
    <li>
      <a href='{{ path("month-index", year=m.year, month=m.month) }}'>
        {{m.strftime('%B')}}
      </a>
    </li>
    {% endwith %}
  {% endfor %}
</ol>
```

Create a `calendar_month.html` template:

```html
<h1>Entries for {{month.strftime('%B %Y')}}</h1>

<ol>
{% for page in pages %}
  <li>
    <a href='{{page.path}}'>{{page.title}}</a>
  </li>
{% endfor %}
</ol>
```

## Add navigation links

Add the following to your `generate.py`:

```python
def global_context(self):
    return {
        'dates': self.flourish.publication_dates,
    }

GLOBAL_CONTEXT = global_context
```

This makes a variable `global.dates` available to all of your templates, which
contains a structure that lists all years, months and days that have
associated source objects.

Lastly, add something like this to your template(s) to link to the
date-based pages:

```html
<nav>
  <ul>
    {% for year in global.dates %}
      <li>
        <a href='/{{year.year}}/'>{{year.year}}</a>
      </li>
    {% endfor %}
  </ul>
</nav>
```

Adjusting the content and styling of the generated navigation and index pages
is left up to you. There is also a day-based page generator if you would
like to have finer-grained archives, see their
[documentation](/api-flourish-generators-calendar/).
