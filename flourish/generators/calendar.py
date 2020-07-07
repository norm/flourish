from datetime import date

from flourish.generators.base import IndexGenerator


class CalendarGenerator(IndexGenerator):
    order_by = 'published'


class CalendarDayGenerator(CalendarGenerator):
    template_name = 'calendar_day.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['day'] = date(
            day=int(self.tokens['day']),
            month=int(self.tokens['month']),
            year=int(self.tokens['year']),
        )
        return _context


class CalendarMonthGenerator(CalendarGenerator):
    template_name = 'calendar_month.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['month'] = date(
            day=int(1),
            month=int(self.tokens['month']),
            year=int(self.tokens['year']),
        )
        dates = self.source_objects.publication_dates
        _context['publication_dates'] = dates[0]['months'][0]['days']
        return _context


class CalendarYearGenerator(CalendarGenerator):
    template_name = 'calendar_year.html'

    def get_context_data(self):
        _context = super().get_context_data()
        _context['year'] = date(
            day=1,
            month=1,
            year=int(self.tokens['year']),
        )
        dates = self.source_objects.publication_dates
        _context['publication_dates'] = dates[0]['months']
        return _context
