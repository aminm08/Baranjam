import numpy as np
import math


def get_client_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_done_jobs_and_their_dates(request):
    labels, data = [], []
    user_done_dates = [str(job.user_done_date) for job in
                       request.user.jobs.filter(is_done=True).order_by('user_done_date')]
    for date in user_done_dates:
        if date not in labels:
            labels.append(date)

    data = [user_done_dates.count(i) for i in labels]
    return labels, data


def get_daily_hour_spent(request, labels):
    spent_time = []
    for date in labels:
        time = 0
        user_jobs = request.user.jobs.filter(is_done=True, user_done_date=date)
        for job in user_jobs:
            if job.duration:
                time += job.duration.hour + job.duration.minute / 60
        spent_time.append(time)

    return spent_time


def get_total_hours_spent(request):
    jobs = request.user.jobs.filter(is_done=True)
    durations = [str(i.duration) for i in jobs if i.duration]

    sumTime = 0
    for time in durations:
        h, m, s = map(int, time.split(':'))
        sumTime += s + m * 60 + h * 3600

    sumTime, s = divmod(sumTime, 60)
    h, m = divmod(sumTime, 60)

    return h, m


def get_user_today_status(data):
    today_status = data[-1] - math.ceil(np.mean(data))
    if today_status < 0:
        today_status = f'{abs(today_status)} job away from average'
        arrow = 'falling_arrow'
    elif today_status == 0:
        today_status = 'you are on average'
        arrow = 'rising_arrow'
    else:
        today_status = f'{today_status} job up the average'
        arrow = 'rising_arrow'
    return today_status, arrow


def get_most_productive_day_info(data, spent_time, labels):
    max_spent_time_index = spent_time.index(max(spent_time))
    productive_day_job_count = data[max_spent_time_index]
    productive_day_hours_spent = spent_time[max_spent_time_index]
    productive_day_date = labels[max_spent_time_index]
    return productive_day_date, productive_day_job_count, productive_day_hours_spent
