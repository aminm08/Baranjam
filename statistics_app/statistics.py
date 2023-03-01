import numpy as np
import math
from datetime import date, datetime
from jalali_date import date2jalali
from django.utils.translation import gettext as _


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

    @staticmethod
    def convert_done_dates_to_jalali_date(done_dates):
        converted_label = []
        for done_date in done_dates:
            dt = datetime.strptime(done_date, "%Y-%m-%d")
            converted_label.append(str(date2jalali(dt)))
        return converted_label

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

    # gets done jobs count by the number of available done dates in all done dates
    def get_done_jobs_count_per_day(self, done_dates):
        daily_job_done = []
        for done_date in done_dates:
            daily_job_done.append(self.all_done_dates.count(done_date))
        return daily_job_done

    def get_done_jobs_in_range(self):
        if self._range_date[0] == "all":
            return self.all_done_jobs
        return self.all_done_jobs.filter(user_done_date__range=self._range_date)


class Hours(Analytics):
    # extracts the amount of spent time of given done jobs
    @staticmethod
    def get_hours_spent(done_jobs):
        hours_spent = 0
        for job in done_jobs:
            if job.duration:
                hours_spent += job.duration.hour + job.duration.minute / 60
        return round(hours_spent, 2)

    def get_hours_per_job_in_general_date(self):
        return [float(job.duration.hour + job.duration.minute / 60) for job in self.get_tasks_done_in_general_date() if
                job.duration]

    def get_hours_spent_per_day(self, done_dates):
        spent_time = []
        for done_date in done_dates:
            time = 0
            for job in self.request.user.jobs.filter(is_done=True, user_done_date=done_date):
                if job.duration:
                    time += job.duration.hour + job.duration.minute / 60
            spent_time.append(round(time, 3))
        return spent_time

    def get_general_date_hours_spent(self):
        return self.get_hours_spent(self.get_tasks_done_in_general_date())

    def get_total_hours_spent(self):
        return self.get_hours_spent(self.all_done_jobs)


class DashBoard(DoneJobs, Hours):

    def get_user_jobs_status(self):
        # gets the mean of all done jobs to compare done jobs of general date

        done_jobs = self.get_done_jobs_count_per_day(self.all_distinct_done_dates)
        done_jobs_mean = math.ceil(np.mean(done_jobs))
        status = self.get_tasks_done_in_general_date().count() - done_jobs_mean
        percentage = status * 100 / done_jobs_mean
        if status < 0:
            status = _('%s jobs away from average' % abs(status))
            arrow = 'falling_arrow'
        elif status == 0:
            status = _('you are on average')
            arrow = 'rising_arrow'
        else:
            status = _('%s jobs up the average' % status)
            arrow = 'rising_arrow'
        return round(percentage, 2), arrow, status

    def get_user_hours_spent_status(self):
        hours_spent = self.get_hours_spent_per_day(self.all_distinct_done_dates)
        hours_spent_mean = math.ceil(np.mean(hours_spent))
        status = self.get_general_date_hours_spent() - hours_spent_mean
        percentage = status * 100 / hours_spent_mean

        if status < 0:
            status = _('%s hours away from average' % abs(status))
            arrow = 'falling_arrow'
        elif status == 0:
            status = _('you are on average')
            arrow = 'rising_arrow'
        else:
            status = _('%s hours up the average' % status)
            arrow = 'rising_arrow'
        return round(percentage, 2), arrow, status

    def get_most_productive_day_info(self):  # replace
        spent_hours = self.get_hours_spent_per_day(self.get_done_dates_in_range())
        data, labels = self.get_done_jobs_count_per_day(self.get_done_jobs_in_range()), self.get_done_dates_in_range()
        if spent_hours:
            max_spent_time_index = spent_hours.index(max(spent_hours))
        elif data:
            max_spent_time_index = data.index(max(data))
        else:
            return None, None, None

        return (date2jalali(datetime.strptime(labels[max_spent_time_index], "%Y-%m-%d")),
                round(spent_hours[max_spent_time_index], 2), data[max_spent_time_index],)

    def get_goal_progress_percentage(self):
        goals = self.request.user.goals.all()
        result = {}
        for goal in goals:
            target_jobs, target_hours = goal.jobs, goal.hours
            if goal.measure == 'd':
                current_jobs_count = self.get_tasks_done_in_general_date().count()
                current_spent_hours = self.get_general_date_hours_spent()
                job_percentage = round((current_jobs_count * 100) / target_jobs, 2)
                hours_percentage = round((current_spent_hours * 100) / target_hours, 2)
                result[str(goal.id)] = [goal.get_measure_display(), job_percentage, hours_percentage]

        return result
