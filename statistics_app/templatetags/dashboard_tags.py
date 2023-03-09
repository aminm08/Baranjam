from django.template import Library
from datetime import date, datetime
from jalali_date import date2jalali
from django.utils.translation import gettext as _

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


@register.filter()
def get_status_arrow(status):
    if status == 0 or status > 0:
        return 'rising_arrow'
    return 'falling_arrow'


@register.filter()
def get_verbose_status(status, key_word: str):
    if status < 0:
        status = _('%s %s away from average' % (abs(status), key_word))
    elif status == 0:
        status = _('you are on average')
    else:
        status = _('%s %s up the average' % (status, key_word))
    return status
