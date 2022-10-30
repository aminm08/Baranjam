from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


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

    # -----------------HOMEPAGE--------------
    def test_homepage_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_by_name(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_used_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage.html')

    # def test_homepage_content(self):
    #     response = self.client.get(reverse('homepage'))
    #     self.assertContains(response, 'اپلیکیشن')

    # ------------------ABOUT US--------------

    def test_about_url(self):
        response = self.client.get('/about_us/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_by_name(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_about_used_template(self):
        response = self.client.get(reverse('about_us'))
        self.assertTemplateUsed(response, 'about_us.html')

    def test_about_content(self):
        response = self.client.get(reverse('about_us'))
        self.assertContains(response, 'Hi')

    # -----------------CONTACT US-----------------

    def test_contact_url(self):
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)

    def test_contact_url_by_name(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)

    def test_contact_used_template(self):
        response = self.client.get(reverse('contact_us'))
        self.assertTemplateUsed(response, 'contact_us.html')

    def test_contact_content(self):
        response = self.client.get(reverse('contact_us'))
        self.assertContains(response, 'You can contact me using :')
        self.assertContains(response, 'my github account')

    # -------------DASHBOARD------------------------

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

    # def test_dashboard_content(self):
    #     self.client.login(email=self.email, password=self.password)
    #     response = self.client.get(reverse('dashboard'))
    #     self.assertContains(response, 'داشبورد')
    #     self.assertContains(response, 'تمام کارهایی که تا الان انجام دادی')
