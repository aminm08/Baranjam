import numpy as np
import math
from datetime import date, datetime
from jalali_date import date2jalali


class Analytics:
    """
    gets basic data ready to
    process in higher levels
    """

    def __init__(self, request, range_date: tuple, general_date):
        self.request = request
        self.today_jobs_done = request.user.jobs.filter(is_done=True, user_done_date=date.today())
        self.all_done_jobs = self.request.user.jobs.filter(is_done=True).order_by('user_done_date')

        self._range_date = range_date
        self.general_date = general_date
        self.all_done_dates = self.extract_done_dates(self.all_done_jobs)
        self.all_distinct_done_dates = sorted(set(self.all_done_dates))

    @staticmethod
    def extract_done_dates(job_list):
        return [str(job.user_done_date) for job in job_list]

    # returns a list of distinct done dates in chosen range
    def get_done_dates_in_range(self):
        if self._range_date[0] == "all":
            return self.all_distinct_done_dates
        data = self.extract_done_dates(self.all_done_jobs.filter(user_done_date__range=self._range_date))
        labels = sorted(set(data), key=self.all_done_dates.index)  # replace it
        return list(labels)

    def get_tasks_done_in_general_date(self):
        return self.request.user.jobs.filter(is_done=True, user_done_date=self.general_date)

    def get_done_jobs_titles_by_general_date(self):
        return [job.text for job in self.get_tasks_done_in_general_date() if job.duration]


class DoneJobs(Analytics):
    def done_job_per_day(self, all_dates=False):
        daily_job_done = []

        done_dates = self.all_distinct_done_dates if all_dates else self.get_done_dates_in_range()

        for done_date in done_dates:
            daily_job_done.append(self.all_done_dates.count(done_date))

        return daily_job_done


class Hours(Analytics):

    def hours_all(self):
        hours_spent = 0
        for job in self.all_done_jobs:
            if job.duration:
                hours_spent += job.duration.hour + job.duration.minute / 60
        return hours_spent

    def get_hours_per_job_in_general_date(self):
        return [float(job.duration.hour + job.duration.minute / 60) for job in self.get_tasks_done_in_general_date() if
                job.duration]

    def hours_per_day(self, all_dates=False):
        spent_time = []
        done_dates = self.all_distinct_done_dates if all_dates else self.get_done_dates_in_range()

        for done_date in done_dates:
            time = 0
            for job in self.request.user.jobs.filter(is_done=True, user_done_date=done_date):
                if job.duration:
                    time += job.duration.hour + job.duration.minute / 60
            spent_time.append(time)

        return spent_time

    def get_general_date_hours_spend(self):
        hours = 0
        for job in self.get_tasks_done_in_general_date():
            if job.duration:
                hours += (job.duration.hour + job.duration.minute / 60)

        return round(hours, 2)


class DashBoard(DoneJobs, Hours):

    def get_user_jobs_status(self):
        # gets the mean of all done jobs to compare done jobs of given date

        done_jobs = self.done_job_per_day(all_dates=True)

        status = self.get_tasks_done_in_general_date().count() - math.ceil(np.mean(done_jobs))
        if status < 0:
            status = f'{abs(status)} jobs away from average'
            arrow = 'falling_arrow'
        elif status == 0:
            status = 'you are on average'
            arrow = 'rising_arrow'
        else:
            status = f'{status} jobs up the average'
            arrow = 'rising_arrow'
        return status, arrow

    def get_user_hours_spent_status(self):
        hours_spent = self.hours_per_day(all_dates=True)

        status = self.get_general_date_hours_spend() - math.ceil(np.mean(hours_spent))

        if status < 0:
            status = f'{abs(status)} hours away from average'
            arrow = 'falling_arrow'
        elif status == 0:
            status = 'you are on average'
            arrow = 'rising_arrow'
        else:
            status = f'{status} hours up the average'
            arrow = 'rising_arrow'
        return status, arrow

    def get_most_productive_day_info(self):
        spent_hours = list(self.hours_per_day())
        data, labels = list(self.done_job_per_day()), list(self.get_done_dates_in_range())
        if spent_hours:
            max_spent_time_index = spent_hours.index(max(spent_hours))
        elif data:
            max_spent_time_index = data.index(max(data))
        else:
            return None, None, None

        return data[max_spent_time_index], round(spent_hours[max_spent_time_index], 2), labels[max_spent_time_index]
