import numpy as np
import math
from datetime import date


class Analytics:

    def __init__(self, request):
        self.request = request
        self.today_jobs_done = request.user.jobs.filter(is_done=True, user_done_date=date.today())
        self.all_done_jobs = self.request.user.jobs.filter(is_done=True).order_by('user_done_date')

    def get_done_dates(self):
        labels = []
        for job in self.all_done_jobs:
            if str(job.user_done_date) not in labels:
                labels.append(str(job.user_done_date))
        return labels

    def get_job_done_each_day(self):
        daily_job_done = []
        durations = [str(job.user_done_date) for job in self.all_done_jobs]
        for date in self.get_done_dates():
            daily_job_done.append(durations.count(date))

        return daily_job_done

    def get_today_hours_spent(self):
        hours = 0
        for job in self.today_jobs_done:
            hours += (job.duration.hour + job.duration.minute / 60)

        return round(hours, 2)

    def get_today_chart(self):
        today_done_jobs_titles = [i.text for i in self.today_jobs_done]
        hours_spent = [float(str(i.duration.hour + i.duration.minute / 60)) for i in self.today_jobs_done]
        return today_done_jobs_titles, hours_spent

    def get_daily_hour_spent(self):
        spent_time = []
        for date in self.get_done_dates():
            time = 0
            for job in self.request.user.jobs.filter(is_done=True, user_done_date=date):
                if job.duration:
                    time += job.duration.hour + job.duration.minute / 60
            spent_time.append(time)

        return spent_time

    def get_total_hours_spent(self):
        jobs = self.request.user.jobs.filter(is_done=True)
        hours_spent = 0
        for job in jobs:
            if job.duration:
                hours_spent += job.duration.hour + job.duration.minute / 60

        return hours_spent

    def get_user_today_status(self):
        done_jobs = self.get_job_done_each_day()
        today_status = self.today_jobs_done.count() - math.ceil(np.mean(done_jobs))
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

    def get_most_productive_day_info(self):
        spent_hours = list(self.get_daily_hour_spent())
        data, labels = list(self.get_job_done_each_day()), list(self.get_done_dates())
        if spent_hours:
            max_spent_time_index = spent_hours.index(max(spent_hours))
        elif data:
            max_spent_time_index = data.index(max(data))
        else:
            return None, None, None

        return data[max_spent_time_index], round(spent_hours[max_spent_time_index], 2), labels[max_spent_time_index]
