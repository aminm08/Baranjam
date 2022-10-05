from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthenticationPagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = 'myusername@user.com'
        cls.password = 'myusername123'

        cls.credentials = {
            'login': cls.email,
            'password': cls.password,
        }

        cls.user1 = get_user_model().objects.create_user(
            username=cls.email,
            email=cls.email,
            password=cls.password,
        )

    # signup
    def test_sign_up_urls_by_name(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        self.assertEqual(get_user_model().objects.all()[0].check_password(self.password), True)

    # login

    def test_login_url(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_by_name(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        response = self.client.post(reverse('account_login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

    # logout

    def test_logout_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url_redirect_anonymous_user(self):
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 302)

    # profile
    def test_profile_urls_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
