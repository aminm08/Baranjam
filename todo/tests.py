from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Todo, Job
from datetime import date, time


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
            user_time='10:12',

        )
        cls.job2 = Job.objects.create(
            text='job2',
            todo=cls.todo_list1,
            user=cls.user1,
            is_done=True
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
            {'name': 'my_test_todo'},
            follow=True,
        )
        self.assertEqual(Todo.objects.last().name, 'my_test_todo')

    def test_user_todo_lists_add_page_redirect_get_request(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('add_todo'))
        self.assertEqual(response.status_code, 405)

    # delete todo
    def test_delete_todo_page_not_allow_get_request(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('todo_delete', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 405)

    def test_todo_delete_page_permission_deny_on_not_owner_users(self):
        self.client.login(email='testuser2@test.com', password=self.password)
        response = self.client.post(reverse('todo_delete', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 403)

    # sorry I had to do 2 tests in 1 case to prevent duplication
    def test_todo_delete_from_db_and_redirect_back(self):
        self.temporary_todo = Todo.objects.create(name='todo2', user=self.user1)
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('todo_delete', args=[self.temporary_todo.id]))
        self.assertFalse(Todo.objects.filter(name='todo2'))
        self.assertEqual(response.status_code, 302)

    # todolist details
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

    def test_login_redirect_from_todo_list_url(self):
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertEqual(response.status_code, 302)

    def test_todo_list_template(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertTemplateUsed(response, 'todo/todo_list.html')

    def test_todo_list_add_job_form(self):
        self.client.login(email=self.email, password=self.password)
        data = {
            'text': 'my_test_job',
            'user_date': '1401-07-14',
            'user_time': '12:55:00',
        }
        response = self.client.post(
            f'/todo/job/create/{self.todo_list1.pk}/',
            data,
            follow=True
        )

        self.assertEqual(Job.objects.last().text, 'my_test_job')

    def test_todo_list_show_added_job(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url())
        self.assertContains(response, self.job1.text)
        self.assertContains(response, self.job2.text)
        self.assertContains(response, Job.objects.last().text)

    # job delete

    def test_job_delete_page_not_allow_get_request(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('job_delete', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 405)

    def test_job_delete_page_permission_deny_on_not_owner_users(self):
        self.client.login(email='testuser2@test.com', password=self.password)
        response = self.client.post(reverse('job_delete', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 403)

    def test_is_job_deleted_from_db(self):
        self.temporary_job = Job.objects.create(text='job2', user=self.user1, todo=self.todo_list1)
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('job_delete', args=[self.temporary_job.id]))
        self.assertFalse(Todo.objects.filter(name='job2'))

    # job update

    def test_job_update_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.todo_list1.get_absolute_url() + str(self.job1.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_job_update_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('job_update', args=[self.todo_list1.get_signed_pk(), self.job1.id]))
        self.assertEqual(response.status_code, 200)

    def test_job_update_permission_deny_on_now_owner(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.get(reverse('job_update', args=[self.todo_list1.get_signed_pk(), self.job1.id]))
        self.assertEqual(response.status_code, 403)

    def test_job_update_form(self):
        self.client.login(email=self.email, password=self.password)
        data = {'text': 'new_update', 'user_date': '1401-07-14', 'user_time': '12:55:00', }
        self.client.post(reverse('job_update', args=[self.todo_list1.get_signed_pk(), self.job1.id]), data, follow=True)
        self.assertTrue(Job.objects.filter(text='new_update').exists())

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

    def test_todo_update_name_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('update_todo_name', args=[self.todo_list1.id]), {'name': 'new_todo'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.last().name, 'new_todo')

    # attention: this test deletes all jobs of todo_list_1
    def test_todo_apply_options_functionality(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('apply_todo_actions', args=[self.todo_list1.id]), {'action': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.todo_list1.jobs.exists(), False)

    def test_todo_apply_options_permission_deny_on_not_owners(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.post(reverse('apply_todo_actions', args=[self.todo_list1.id]), {'action': '1'})
        self.assertEqual(response.status_code, 403)
