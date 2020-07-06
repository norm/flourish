from datetime import date


def ordinal(value):
    if value in (11, 12, 13):
        return 'th'
    last = value % 10
    if last == 1:
        return 'st'
    if last == 2:
        return 'nd'
    if last == 3:
        return 'rd'
    return 'th'


def month_name(value):
    return date(1970, value, 1).strftime('%B')
