from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from group_lists.models import GroupList
from todo.models import Todo, Job
from .models import Invitation


class GroupListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ownerUserEmail = 'myusername@user.com'
        cls.adminUser2Email = 'user2admin@ser.com'
        cls.memberUserEmail = 'testuser2@test.com'
        cls.regularUserEmail = 'hello@hello.com'
        cls.username = 'group_admin_owner'
        cls.username4 = 'group_admin_user_2'
        cls.username2 = 'group_member_user'
        cls.username3 = 'regular_user'
        cls.password = 'myusername123'

        cls.ownerUser = get_user_model().objects.create_user(
            username=cls.username,
            email=cls.ownerUserEmail,
            password=cls.password,
        )
        cls.memberUser = get_user_model().objects.create_user(
            username=cls.username2,
            email=cls.memberUserEmail,
            password=cls.password,
        )
        cls.regularUser = get_user_model().objects.create_user(
            username=cls.username3,
            email=cls.regularUserEmail,
            password=cls.password,
        )
        cls.adminUser = get_user_model().objects.create_user(
            username=cls.username4,
            email=cls.adminUser2Email,
            password=cls.password,
        )
        cls.todo_list1 = Todo.objects.create(
            name='todo_test',
            user=cls.ownerUser
        )
        cls.reg_user_todo_list = Todo.objects.create(
            name='todo_test2',
            user=cls.regularUser
        )

        cls.job1 = Job.objects.create(
            text='test_job',
            todo=cls.todo_list1,
            user=cls.ownerUser,
            user_date='1401-08-10',
            duration='1:10:00',

        )
        cls.group_list_1 = GroupList.objects.create(
            title='group_1',
            description='hello desc',
            enable_chat=True,
        )
        cls.group_list_1.todos.add(cls.todo_list1)
        cls.group_list_1.admins.add(cls.ownerUser)
        cls.group_list_1.admins.add(cls.adminUser)
        cls.group_list_1.members.add(cls.memberUser)

    # invite new members
    def test_invite_members_denies_not_admin_users(self):
        self.client.login(email=self.memberUserEmail, password=self.password)
        response = self.client.post(reverse('invite_members', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_invite_members_does_not_send_inv_for_already_joined_users(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        self.client.post(reverse('invite_members', args=[self.group_list_1.id]), {'': '', str(self.memberUser.id): ''})
        self.assertFalse(GroupList.objects.last().user_has_invitation(receiver=self.memberUser, sender=self.ownerUser))

    def test_invite_members_does_not_send_inv_twice_for_one_user(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        Invitation.objects.create(group_list=self.group_list_1, user_receiver=self.regularUser,
                                  user_sender=self.ownerUser)
        self.client.post(reverse('invite_members', args=[self.group_list_1.id]), {'': '', str(self.regularUser.id): ''})
        self.assertEqual(Invitation.objects.count(), 1)

    def test_invite_members_functionality(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        user_ids_inv = {'': '', str(self.regularUser.id): ''}
        response = self.client.post(reverse('invite_members', args=[self.group_list_1.id]), user_ids_inv)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(GroupList.objects.last().user_has_invitation(receiver=self.regularUser, sender=self.ownerUser))

    # accept invite
    def test_accept_invite_denies_not_receiver_users_request(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        inv = Invitation.objects.create(group_list=self.group_list_1, user_sender=self.adminUser,
                                        user_receiver=self.regularUser)
        response = self.client.post(reverse('accept_inv', args=[self.group_list_1.id, inv.id]))
        self.assertEqual(response.status_code, 403)

    def test_accept_invite_functionality(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        inv = Invitation.objects.create(group_list=self.group_list_1, user_sender=self.adminUser,
                                        user_receiver=self.regularUser)
        response = self.client.post(reverse('accept_inv', args=[self.group_list_1.id, inv.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.group_list_1.is_in_group(self.regularUser))
        self.assertEqual(Invitation.objects.count(), 0)

    # foreign invite show info

    def test_foreign_invitation_show_info_url_by_name(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.get(reverse('foreign_inv_show_info', args=[self.group_list_1.get_signed_pk()]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group_list_1.title)

    def test_foreign_invitation_show_info_url(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.get(f'/invitations/invite/accept_foreign/{self.group_list_1.get_signed_pk()}/')
        self.assertEqual(response.status_code, 200)

    # accept foreign invitation

    def test_accept_foreign_invite_redirect_unauthenticated_users(self):
        response = self.client.post(reverse('accept_inv_foreign', args=[self.group_list_1.id]))
        redirect_url = f'/accounts/login/?next=/group_lists/invite/accept_foreign/{self.group_list_1.get_signed_pk()}/'
        self.assertRedirects(response, redirect_url, status_code=302)

    def test_accept_foreign_invite_functionality(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.post(reverse('accept_inv_foreign', args=[self.group_list_1.id]))
        self.assertRedirects(response, self.group_list_1.get_absolute_url(), status_code=302)
        self.assertTrue(self.group_list_1.is_member(self.regularUser))
        self.assertFalse(self.group_list_1.is_admin(self.regularUser))

    # group invite user search

    def test_group_invite_user_search_denies_not_admin_request(self):
        self.client.login(email=self.memberUserEmail, password=self.password)
        response = self.client.post(reverse('search_users_view', args=[self.group_list_1.id]), {'series': 'a'})
        self.assertEqual(response.status_code, 403)

    def test_group_invite_user_search_functionality_with_no_data(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.post(reverse('search_users_view', args=[self.group_list_1.id]), {'series': 'No data!!'})
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {"data": "No data"})

    def test_group_invite_user_search_functionality(self):
        # response has to contain not member users result
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.post(reverse('search_users_view', args=[self.group_list_1.id]), {'series': 'a'})
        self.assertJSONEqual(str(response.content, encoding='utf-8'),
                             {"data": [{
                                 "pk": self.regularUser.id,
                                 "username": self.regularUser.username,
                                 "image": self.regularUser.get_profile_pic_or_blank(),
                             }]})
