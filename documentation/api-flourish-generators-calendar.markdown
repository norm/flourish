# CalendarGenerator

`CalendarGenerator` is the base class for the date-based generators. It
inherits from `IndexGenerator`, and orders sources by date of publication.
There are three generators than use `CalendarGenerator` as their base.


## CalendarYearGenerator

### Context variables

* `year` — a [`datetime.date`][dtd] object set to Jan 1st of the year


## CalendarMonthGenerator

### Context variables

* `month` — a [`datetime.date`][dtd] object set to 1st day of the month


## CalendarDayGenerator

### Context variables

* `day` — a [`datetime.date`][dtd] object set to the day


[dtd]: https://docs.python.org/3/library/datetime.html#datetime.date
