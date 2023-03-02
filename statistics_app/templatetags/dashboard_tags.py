from django.template import Library

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
