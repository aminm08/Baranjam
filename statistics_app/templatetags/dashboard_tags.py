from django.template import Library
from datetime import date, datetime
from jalali_date import date2jalali

register = Library()


@register.filter()
def extract_hours_and_minutes(h: float):
    if h:
        hours = int(h)
        minutes = int((h - hours) * 60)
        return "%s h %s m" % (hours, minutes)
    return 0


@register.filter()
def get_obj_by_index(iterable, index: int):
    return iterable[index]


@register.filter()
def simplify_date(_date: datetime):
    if _date == date.today():
        return 'Today'
    return date2jalali(_date)
