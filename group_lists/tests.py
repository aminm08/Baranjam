from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import GroupList

from pages.models import Invitation
from todo.models import Todo, Job


class GroupListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = 'myusername@user.com'
        cls.email2 = 'testuser2@test.com'
        cls.email3 = 'hello@hello.com'
        cls.username = 'testuser2'
        cls.username2 = 'user3'
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
        cls.user3 = get_user_model().objects.create_user(
            username=cls.username2,
            email=cls.email3,
            password=cls.password,
        )
        cls.todo_list1 = Todo.objects.create(
            name='todo_test',
            user=cls.user1
        )
        cls.todo_list2 = Todo.objects.create(
            name='todo_test2',
            user=cls.user1
        )

        cls.job1 = Job.objects.create(
            text='test_job',
            todo=cls.todo_list1,
            user=cls.user1,
            user_date='1401-08-10',
            user_time='10:12',

        )
        cls.group_list_1 = GroupList.objects.create(todo=cls.todo_list1)
        cls.group_list_1.users.add(cls.user1)
        cls.group_list_1.users.add(cls.user2)

    def test_user_group_lists_page_url(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get('/group_lists/')
        self.assertEqual(response.status_code, 200)

    def test_user_group_lists_page_url_by_name(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('group_lists'))
        self.assertEqual(response.status_code, 200)

    def test_user_group_lists_template_used(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('group_lists'))
        self.assertTemplateUsed(response, 'group_lists/add_group_list.html')

    def test_user_group_lists_show_content_only_to_not_owner_user_in_page(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.get(reverse('group_lists'))
        self.assertContains(response, self.group_list_1.todo.name)
        self.assertContains(response, '2')
        self.assertContains(response, self.group_list_1.todo.user.username)

    def test_user_group_list_dont_show_list_to_owner_in_page(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('group_lists'))
        self.assertNotContains(response, self.group_list_1.todo.name)

    def test_user_group_list_leave_group(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.post(reverse('group_lists'), {'': '', str(self.group_list_1.id): ['']})
        self.assertFalse(self.user2 in self.group_list_1.users.all())

    def test_add_group_list_and_send_invitations(self):
        self.client.login(email=self.email, password=self.password)
        post_data = {
            'users': self.username,
            'todo': self.todo_list2.id,
        }
        response = self.client.post(reverse('add_group_list'), post_data, follow=True)
        self.assertEqual(GroupList.objects.last().todo.name, self.todo_list2.name)
        self.assertTrue(Invitation.objects.exists())

    def test_add_group_or_invite_only_accept_owner_user_demand(self):
        self.client.login(email=self.email2, password=self.password)
        post_data = {
            'users': self.username,
            'todo': self.todo_list2.id,
        }
        response = self.client.post(reverse('add_group_list'), post_data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_user_accept_invite_to_join_group(self):
        self.client.login(email=self.email3, password=self.password)
        temporary_todo = Todo.objects.create(name='temp_todo', user=self.user1)
        temporary_group_list = GroupList.objects.create(todo=temporary_todo)

        temporary_inv = Invitation.objects.create(user_receiver=self.user3, user_sender=self.user1,
                                                  group_list=temporary_group_list)

        response = self.client.post(reverse('accept_inv', args=[temporary_group_list.id, temporary_inv.id]),
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user3 in temporary_group_list.users.all())
        self.assertFalse(Invitation.objects.filter(group_list=temporary_group_list).exists())
        temporary_group_list.delete()
        temporary_todo.delete()

    def test_user_accept_invite_to_join_group_permission_deny_on_not_receiver_users(self):
        self.client.login(email=self.email, password=self.password)
        temporary_todo = Todo.objects.create(name='temp_todo', user=self.user1)
        temporary_group_list = GroupList.objects.create(todo=temporary_todo)

        temporary_inv = Invitation.objects.create(user_receiver=self.user3, user_sender=self.user1,
                                                  group_list=temporary_group_list)

        response = self.client.post(reverse('accept_inv', args=[temporary_group_list.id, temporary_inv.id]),
                                    follow=True)
        self.assertEqual(response.status_code, 403)

        temporary_group_list.delete()
        temporary_todo.delete()

    def test_remove_user_from_group_list(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('delete_group_user', args=[self.todo_list1.id]),
                                    {'': '', str(self.user2.id): ['']})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user2 not in self.group_list_1.users.all())

    def test_remove_user_from_group_page_accept_only_post(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('delete_group_user', args=[self.todo_list1.id]))
        self.assertEqual(response.status_code, 405)

    def test_remove_user_from_group_page_is_not_deleting_owner_user(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('delete_group_user', args=[self.todo_list1.id]),
                                    {'': '', str(self.user1.id): ['']})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user1 in self.group_list_1.users.all())

    def test_remove_user_from_group_list_is_not_happening_by_not_owner_users(self):
        self.client.login(email=self.email2, password=self.password)
        response = self.client.post(reverse('delete_group_user', args=[self.todo_list1.id]),
                                    {'': '', str(self.user2.id): ['']})
        self.assertEqual(response.status_code, 403)

    def test_remove_user_from_group_list_only_works_on_group_lists(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('delete_group_user', args=[self.todo_list2.id]),
                                    {'': '', str(self.user2.id): ['']})
        self.assertEqual(response.status_code, 403)
