from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from jalali_date import date2jalali
from .models import Todo, Job


class TodoPagesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.email = 'myusername@user.com'
        cls.email2 = 'testuser2@test.com'
        cls.username = 'testuser2'
        cls.password = 'myusername123'

        cls.user1 = get_user_model().objects.create_user(
            username=cls.email,
            email=cls.email,
            password=cls.password,
        )
        cls.user2 = get_user_model().objects.create_user(
            username=cls.username,
            email=cls.email2,
            password=cls.password,
        )

        cls.todo_list1 = Todo.objects.create(
            name='todo_test',
            user=cls.user1
        )

        cls.job1 = Job.objects.create(
            text='test_job',
            todo=cls.todo_list1,
            user=cls.user1,
            user_date='1401-08-10',
            duration='1:00',

        )
        cls.job2 = Job.objects.create(
            text='job2',
            todo=cls.todo_list1,
            user=cls.user1,
            is_done=True,
            duration='0:30',
            user_done_date='1401-10-8'
        )

    # user_todos
    def test_user_todo_lists_page_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get('/todo/')
        self.assertEqual(response.status_code, 200)

    def test_user_todo_lists_page_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('user_todos'))
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_anonymous_user_from_todos(self):
        response = self.client.get(reverse('user_todos'))
        self.assertEqual(response.status_code, 302)

    def test_user_todo_lists_page_template(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('user_todos'))
        self.assertTemplateUsed(response, 'todo/user_todos.html')

    def test_user_lists_page_showing_todo(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('user_todos'))
        self.assertContains(response, self.todo_list1.name)

    def test_user_lists_page_finished_jobs_number(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('user_todos'))
        self.assertContains(response, 'finished')
        self.assertContains(response, '1')

    # add todo
    def test_user_todo_lists_add_form(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(
            reverse('add_todo'),
            {'name': 'my_test_todo'})
        self.assertEqual(Todo.objects.last().name, 'my_test_todo')
        self.assertEqual(response.status_code, 302)

    def test_user_todo_lists_add_only_accepts_get_request(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('add_todo'))
        self.assertEqual(response.status_code, 405)

    # delete todo
    def test_delete_todo_page_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(f'/todo/delete/{self.todo_list1.get_signed_pk()}/')
        self.assertEqual(response.status_code, 200)

    def test_delete_todo_page_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('todo_delete', args=[self.todo_list1.get_signed_pk()]))
        self.assertEqual(response.status_code, 200)

    def test_delete_todo_template_used(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('todo_delete', args=[self.todo_list1.get_signed_pk()]))
        self.assertTemplateUsed(response, 'todo/todo_delete.html')

    def test_todo_delete_page_permission_deny_on_not_owner_users(self):
        self.client.login(email='testuser2@test.com', password=self.password)
        response = self.client.post(reverse('todo_delete', args=[self.todo_list1.get_signed_pk()]))
        self.assertEqual(response.status_code, 403)

    def test_todo_delete_from_db_and_redirect_back(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('todo_delete', args=[self.todo_list1.get_signed_pk()]))
        self.assertEqual(Todo.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    # todo-list details
    def test_todo_list_page_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(f'/todo/todo_list/{self.todo_list1.get_signed_pk()}/')
        self.assertEqual(response.status_code, 200)

    def test_todo_list_usl_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('todo_list', args=[self.todo_list1.get_signed_pk()]))
        self.assertEqual(response.status_code, 200)

    def test_todo_list_name_in_page(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertContains(response, self.todo_list1.name)

    def test_login_redirect_from_todo_list_url_for_anonymous(self):
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertEqual(response.status_code, 302)

    def test_todo_list_content_filter_by_done(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url(), {'filter': 'done'})
        self.assertContains(response, self.job2.text)
        self.assertNotContains(response, self.job1.text)

    def test_todo_list_content_filter_by_actives(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url(), {'filter': 'actives'})
        self.assertContains(response, self.job1.text)
        self.assertNotContains(response, self.job2.text)

    def test_todo_list_content_filter_by_all(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url(), {'filter': 'all'})
        self.assertContains(response, self.job1.text)
        self.assertContains(response, self.job2.text)

    def test_todo_list_template(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertTemplateUsed(response, 'todo/todo_list.html')

    def test_todo_list_deny_not_owner_user_permission(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    # test create job
    def test_create_job_view(self):
        self.client.login(email=self.email, password=self.password)
        data = {'text': 'my_test_job', 'user_date': '1401-07-14', 'duration': '1:0', }
        response = self.client.post(f'/todo/job/create/{self.todo_list1.pk}/', data)
        self.assertEqual(Job.objects.last().text, 'my_test_job')
        self.assertEqual(str(date2jalali(Job.objects.last().user_date)), '1401-07-14')
        self.assertEqual(str(Job.objects.last().duration), '01:00:00')
        self.assertEqual(response.status_code, 302)

    def test_create_job_denying_not_owner_users_request(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.post(reverse('job_create', args=[self.todo_list1.id]), {'text': 'my_test_job'})
        self.assertEqual(response.status_code, 403)

    def test_todo_list_show_added_job(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertContains(response, self.job1.text)
        self.assertContains(response, self.job2.text)
        self.assertContains(response, Job.objects.get(text=self.job1.text).get_duration())
        self.assertContains(response, Job.objects.get(text=self.job2.text).get_duration())

    def test_get_duration_method(self):
        self.assertEqual(Job.objects.get(text=self.job1.text).get_duration(), '1 hours ')
        self.assertEqual(Job.objects.get(text=self.job2.text).get_duration(), '30 minutes')

    # job delete

    def test_job_delete_page_not_allow_get_request(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('job_delete', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 405)

    def test_job_delete_page_permission_deny_on_not_owner_users(self):
        self.client.login(email='testuser2@test.com', password=self.password)
        response = self.client.post(reverse('job_delete', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 403)

    def test_job_delete_from_db(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('job_delete', args=[self.job1.id]))
        self.assertFalse(Job.objects.filter(text=self.job1.text))

    # job update

    def test_job_update_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url() + str(self.job1.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_job_update_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('job_update', args=[self.todo_list1.get_signed_pk(), self.job1.id]))
        self.assertEqual(response.status_code, 200)

    def test_job_update_permission_deny_on_not_owner(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.get(reverse('job_update', args=[self.todo_list1.get_signed_pk(), self.job1.id]))
        self.assertEqual(response.status_code, 403)

    def test_job_update_form(self):
        self.client.login(email=self.email, password=self.password)
        data = {'text': 'new_update', 'user_date': '1401-07-14', 'duration': '3:0', }
        response = self.client.post(reverse('job_update', args=[self.todo_list1.get_signed_pk(), self.job1.id]), data)
        self.assertTrue(Job.objects.filter(text='new_update').exists())
        self.assertTrue(Job.objects.filter(duration='03:00:00').exists())
        self.assertEqual(response.status_code, 302)

    def test_job_update_template_used(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('job_update', args=[self.todo_list1.get_signed_pk(), self.job1.id]))
        self.assertTemplateUsed(response, 'todo/update_job.html')

    # todo settings
    def test_todo_settings_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(f'/todo/settings/{self.todo_list1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_todo_settings_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('todo_settings', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 200)

    def test_todo_settings_template_used(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('todo_settings', args=[self.todo_list1.id]))
        self.assertTemplateUsed(response, 'todo/todo_settings.html')

    def test_todo_settings_permission_deny_on_not_owner_users(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.get(reverse('todo_settings', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 403)

    def test_todo_settings_show_the_owner(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('todo_settings', args=[self.todo_list1.id]))
        self.assertContains(response, self.todo_list1.user)

    # change todo name

    def test_todo_update_list_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('update_todo_name', args=[self.todo_list1.id]), {'name': 'new_name'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.last().name, 'new_name')

    def test_todo_update_list_name_denys_not_owner_permission(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.post(reverse('update_todo_name', args=[self.todo_list1.id]), {'name': 'new_name'})
        self.assertEqual(response.status_code, 403)

    # todo apply option
    def test_todo_apply_options_delete_all_jobs(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('apply_todo_actions', args=[self.todo_list1.id]), {'action': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.todo_list1.jobs.exists())

    def test_todo_apply_options_delete_finished_jobs(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('apply_todo_actions', args=[self.todo_list1.id]), {'action': '2'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.todo_list1.jobs.filter(is_done=True).exists())

    def test_todo_apply_options_active_all_jobs(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('apply_todo_actions', args=[self.todo_list1.id]), {'action': '3'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.todo_list1.jobs.filter(is_done=True).exists())

    def test_todo_apply_options_finish_all_jobs(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('apply_todo_actions', args=[self.todo_list1.id]), {'action': '4'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.todo_list1.jobs.filter(is_done=False).exists())

    def test_todo_apply_options_permission_deny_on_not_owners(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.post(reverse('apply_todo_actions', args=[self.todo_list1.id]), {'action': '1'})
        self.assertEqual(response.status_code, 403)

    # todo_list_jobs set status
    def test_set_job_status_to_done(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('job_assign', args=[self.job1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Job.objects.get(text=self.job1.text).is_done)
        self.assertTrue(Job.objects.get(text=self.job1.text).user_done_date)

    def test_set_job_status_to_todo(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('job_assign', args=[self.job2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Job.objects.get(text=self.job2.text).is_done)
        self.assertFalse(Job.objects.get(text=self.job2.text).user_done_date)

    def test_set_job_denys_not_owner_access(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.post(reverse('job_assign', args=[self.job2.id]))
        self.assertEqual(response.status_code, 403)
