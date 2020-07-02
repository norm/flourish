# CalendarGenerator

`CalendarGenerator` is the base class for the date-based generators. It
inherits from `IndexGenerator`, and orders sources by date of publication.
There are three generators than use `CalendarGenerator` as their base.


## CalendarYearGenerator

### Context variables

* `year` — a [`datetime.date`][dtd] object set to Jan 1st of the year
* `publication_dates` — an array of months that have published sources in this
  year. Each object contains a `datetime.date` object for the first of the
  month, and a `days` array of all days within that month that have published
  sources.

    [
        {
            'month': datetime.date(2016, 2, 1),
            'days': [
                datetime.date(2016, 2, 3),
                datetime.date(2016, 2, 12),
                datetime.date(2016, 2, 18),
            ]
        }
    ]

  Most useful to create navigation to only those months with
  publications, rather than all months of the year:

    <ol>
      {% for month in publication_dates %}
        {% with m=month.month %}
        <li>
          <a href='{{ url("month", year=m.year, month=m.month) }}'>
            {{m.strftime('%B')}}
          </a>
        </li>
        {% endwith %}
      {% endfor %}
    </ol>
  
  Or, to include days as well:

    {% for month in publication_dates %}
      <h2>{{month.month.strftime('%B')}}</h2>
      <ol>
        {% for day in month.days %}
          <li>
            <a href='{% "day" year=day.year, month=day.month day=day.day %}'>
              {{day}}
            </a>
          </li>
        {% endfor %}
      </ol>
    {% endfor %}


## CalendarMonthGenerator

### Context variables

* `month` — a [`datetime.date`][dtd] object set to 1st day of the month
* `publication_dates` an array of days in the month that have published
  sources. Useful to link to day-specific pages, rather than listing
  all of the sources for that month:

  <ol>
    {% for day in publication_dates %}
      <li>
        <a href='{% "day" year=day.year, month=day.month day=day.day %}'>
          {{day}}
        </a>
      </li>
    {% endfor %}
  </ol>


## CalendarDayGenerator

### Context variables

* `day` — a [`datetime.date`][dtd] object set to the day


[dtd]: https://docs.python.org/3/library/datetime.html#datetime.date
