from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from todo.models import Todo, Job


class PagesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.email = 'myusername@user.com'
        cls.password = 'myusername123'

        cls.user1 = get_user_model().objects.create_user(
            username=cls.email,
            email=cls.email,
            password=cls.password,
        )

        cls.todo_list1 = Todo.objects.create(
            name='todo_test',
            user=cls.user1
        )

        cls.job2 = Job.objects.create(
            text='job2',
            todo=cls.todo_list1,
            user=cls.user1,
            is_done=True,
            duration='0:30',
            user_done_date='1401-10-8'
        )

    def test_dashboard_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_used_template(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard.html')
