from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AccountsPagesTest(TestCase):
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

    def test_signup_user(self):
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.last().email, self.email)
        self.assertEqual(get_user_model().objects.last().check_password(self.password), True)

    # def test_signup_form(self):# recaptcha
    #     response = self.client.post(reverse('account_signup'),
    #                                 {'username': 'username2', 'email': 'hello@hello.com', 'password1': 'hellopass123',
    #                                  'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'},
    #                                 follow=True)
    #
    #     self.assertEqual(get_user_model().objects.all().count(), 2)
    #     self.assertEqual(get_user_model().objects.last().email, 'hello@hello.com')
    #     self.assertEqual(get_user_model().objects.last().username, 'username2')
    #     self.assertEqual(get_user_model().objects.last().check_password('hellopass123'), True)
    #     get_user_model().objects.last().delete()

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

    def test_profile_form(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('profile'), {'username': 'amin', "email": self.user1.email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user_model().objects.last().username, 'amin')
