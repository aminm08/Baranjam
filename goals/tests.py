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
        cls.regularUserEmail = 'test@test2.com'

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

    # goal create

    def test_goal_create_view_functionality(self):
        self.client.login(email=self.goalOwnerEmail, password=self.password)
        response = self.client.post(reverse('goal_create'), {'measure': 'd', 'jobs': 5, 'hours': 5})
        goal = Goal.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(goal.user, self.goalOwnerUser)
        self.assertEqual(goal.jobs, 5)
        self.assertEqual(goal.hours, 5)
        self.assertEqual(goal.measure, 'd')

    def test_goal_create_view_only_accepts_post_request(self):
        self.client.login(email=self.goalOwnerEmail, password=self.password)
        response = self.client.get(reverse('goal_create'))
        self.assertEqual(response.status_code, 405)

    # goal delete

    def test_goal_delete_only_accepts_post(self):
        self.client.login(email=self.goalOwnerEmail, password=self.password)
        response = self.client.get(reverse('goal_delete', args=[self.goal.id]))
        self.assertEqual(response.status_code, 405)

    def test_goal_delete_denies_not_owner_user_request(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.post(reverse('goal_delete', args=[self.goal.id]))
        self.assertEqual(response.status_code, 403)

    def test_goal_delete_functionality(self):
        self.client.login(email=self.goalOwnerEmail, password=self.password)
        response = self.client.post(reverse('goal_delete', args=[self.goal.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Goal.objects.count(), 0)
