import numpy as np
import math
from datetime import date, datetime


class Analytics:
    """
    gets basic data ready to
    process in higher levels
    """

    def __init__(self, request, range_date: list):
        self.request = request
        self.today_jobs_done = request.user.jobs.filter(is_done=True, user_done_date=date.today())
        self.all_done_jobs = self.request.user.jobs.filter(is_done=True).order_by('user_done_date')
        self._range_date = range_date

        self.all_done_dates = self.extract_done_dates(self.all_done_jobs)

    @staticmethod
    def extract_done_dates(job_list):
        return [str(job.user_done_date) for job in job_list]

    @staticmethod
    def validate_range(range_date):
        """
        makes sure that range is whether ['date', 'date'] or ['all']
        """
        if len(range_date) == 1 and range_date[0] == 'all':
            return True
        elif len(range_date) == 2:
            try:

                datetime.strptime(range_date[0], "%Y-%m-%d")
                datetime.strptime(range_date[1], "%Y-%m-%d")
                return True

            except ValueError:
                return False
        return False

    def get_jobs_in_range(self):
        if self._range_date[0] == "all":
            return self.all_done_jobs
        return self.all_done_jobs.filter(user_done_date__range=self._range_date)

    def get_done_dates(self):

        data = self.extract_done_dates(self.get_jobs_in_range())
        labels = sorted(set(data), key=self.all_done_dates.index)
        return list(labels)

    def get_today_done_jobs_title(self):
        return [i.text for i in self.today_jobs_done if i.duration]


class Hours(Analytics):

    def hours_all(self):
        hours_spent = 0
        for job in self.all_done_jobs:
            if job.duration:
                hours_spent += job.duration.hour + job.duration.minute / 60
        return hours_spent

    def hours_today(self):
        hours = 0
        for job in self.today_jobs_done:
            if job.duration:
                hours += (job.duration.hour + job.duration.minute / 60)

        return round(hours, 2)

    def hours_per_job(self):
        return [float(str(i.duration.hour + i.duration.minute / 60)) for i in self.today_jobs_done if i.duration]

    def hours_per_day(self):
        spent_time = []
        for done_date in self.get_done_dates():
            time = 0
            for job in self.request.user.jobs.filter(is_done=True, user_done_date=done_date):
                if job.duration:
                    time += job.duration.hour + job.duration.minute / 60
            spent_time.append(time)

        return spent_time


class DoneJobs(Analytics):
    def done_job_per_day(self):
        daily_job_done = []
        for done_date in self.get_done_dates():
            daily_job_done.append(self.all_done_dates.count(done_date))

        return daily_job_done


class DashBoard(DoneJobs, Hours):

    def get_user_today_status(self):
        done_jobs = self.done_job_per_day()
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
        spent_hours = list(self.hours_per_day())
        data, labels = list(self.done_job_per_day()), list(self.get_done_dates())
        if spent_hours:
            max_spent_time_index = spent_hours.index(max(spent_hours))
        elif data:
            max_spent_time_index = data.index(max(data))
        else:
            return None, None, None

        return data[max_spent_time_index], round(spent_hours[max_spent_time_index], 2), labels[max_spent_time_index]
