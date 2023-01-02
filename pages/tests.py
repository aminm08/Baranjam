from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from todo.models import Todo, Job
from .models import Contact


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

    def test_homepage_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_by_name(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_used_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage.html')

    def test_about_url(self):
        response = self.client.get('/about_us/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_by_name(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_about_used_template(self):
        response = self.client.get(reverse('about_us'))
        self.assertTemplateUsed(response, 'about_us.html')

    def test_contact_url(self):
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)

    def test_contact_url_by_name(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)

    def test_contact_us_form(self):
        post_data = {
            'full_name': 'amin forouzan',
            'email': 'maf081378@gmail.com',
            'phone_number': '09139321878',
            'message': 'hi'
        }
        response = self.client.post(reverse('contact_us'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.last().full_name, 'amin forouzan')
        self.assertEqual(Contact.objects.last().email, 'maf081378@gmail.com')
        self.assertEqual(Contact.objects.last().phone_number, '09139321878')
        self.assertEqual(Contact.objects.last().message, 'hi')
        self.assertTrue(Contact.objects.last().ip_addr)

    def test_contact_used_template(self):
        response = self.client.get(reverse('contact_us'))
        self.assertTemplateUsed(response, 'contact_us.html')
