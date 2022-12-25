
def get_client_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_done_jobs_by_date(request):

    labels, data = [], []
    user_done_dates = [str(job.user_done_date) for job in
                       request.user.jobs.filter(is_done=True).order_by('user_done_date')]

    for date in user_done_dates:
        if date not in labels:
            labels.append(date)

    data = [user_done_dates.count(i) for i in labels]
    return labels, data
