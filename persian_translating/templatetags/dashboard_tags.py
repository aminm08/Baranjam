from django.template import Library

register = Library()

@register.filter()
def get_completed_jobs(user):
    return user.jobs.filter(is_done=True).count()