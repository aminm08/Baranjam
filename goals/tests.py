from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Goal


class GoalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.goalOwnerUsername = 'test'
        cls.goalOwnerEmail = 'test@test.com'
        cls.password = 'testpass123'

        cls.regularUserUsername = 'test2'
        cls.regularUserEmail = 'test@test.com'

        cls.goalOwnerUser = get_user_model().objects.create_user(
            username=cls.goalOwnerUsername,
            email=cls.goalOwnerEmail,
            password=cls.password,
        )

        cls.regularUser = get_user_model().objects.create_user(
            username=cls.regularUserUsername,
            email=cls.regularUserEmail,
            password=cls.password,
        )

        cls.goal = Goal.objects.create(
            user=cls.goalOwnerUser,
            jobs=10,
            hours=10,
            measure='d'
        )
    #goal create
    def test_goal_create_view_functionality(self):
        self.client.login(email=self.goalOwnerUser, password=self.password)
        response = self.client.post(reverse('goal_create'), {'measure': 'd', 'jobs': 5, 'hours': 5})
        goal = Goal.objects.last()
        self.assertRedirects(response, reverse('dashboard'), status_code=302)
        self.assertEqual(goal.user, self.goalOwnerUser)
        self.assertEqual(goal.jobs, 5)
        self.assertEqual(goal.hours, 5)
        self.assertEqual(goal.measure, 'd')

    def test_goal_create_view_only_accepts_post_request(self):
        self.client.login(email=self.goalOwnerUser, password=self.password)
        response = self.client.get(reverse('goal_create'))
        self.assertEqual(response.status_code, 405)


