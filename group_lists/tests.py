from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import GroupList
from chats.models import OnlineUsers
from .models import Invitation
from todo.models import Todo, Job


class GroupListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ownerUserEmail = 'myusername@user.com'
        cls.adminUser2Email = 'user2admin@ser.com'
        cls.memberUserEmail = 'testuser2@test.com'
        cls.regularUserEmail = 'hello@hello.com'
        cls.username = 'group_admin_user'
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

    def test_group_list_url_by_name_admin_can_see_group_on_list(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(reverse('group_lists'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group_list_1.title)

    def test_group_list_regular_user_cant_see_group_on_list(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.get(reverse('group_lists'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.group_list_1.title)

    def test_group_list_url_member_can_see_group_list(self):
        self.client.login(email=self.memberUserEmail, password=self.password)
        response = self.client.get('/group_lists/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group_list_1.title)

    def test_group_list_shown_members_count(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.get(reverse('group_lists'))
        self.assertContains(response, self.group_list_1.get_all_members_length())

    # delete
    def test_group_delete_url_can_only_be_accessed_by_first_admin(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(reverse('group_delete', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 200)

    def test_group_delete_cant_be_accessed_by_other_admin_users(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.get(reverse('group_delete', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_group_delete_cant_be_accessed_by_member_users(self):
        self.client.login(email=self.memberUserEmail, password=self.password)
        response = self.client.get(reverse('group_delete', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_group_delete_cant_be_accessed_by_regular_users(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.get(reverse('group_delete', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_group_delete_functionality(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.post(reverse('group_delete', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(GroupList.objects.count(), 0)

    def test_group_delete_template_used(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(reverse('group_delete', args=[self.group_list_1.id]))
        self.assertTemplateUsed(response, 'group_lists/group_delete.html')

    # group update

    def test_group_update_view_can_be_accessed_by_admins(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.get(reverse('group_update', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group_list_1.title)

    def test_group_update_view_cant_be_accessed_by_members(self):
        self.client.login(email=self.memberUserEmail, password=self.password)
        response = self.client.get(reverse('group_update', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_group_update_view_cant_be_accessed_by_regular_user(self):
        self.client.login(email=self.memberUserEmail, password=self.password)
        response = self.client.get(reverse('group_update', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_group_update_view_functionality(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        updated_post_credentials = {
            'title': 'updated_title',
            'description': 'new_desc',
            'todos': str(self.todo_list1.id),
        }

        response = self.client.post(reverse('group_update', args=[self.group_list_1.id]), updated_post_credentials)
        updated_group_list = GroupList.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_group_list.title, 'updated_title')
        self.assertEqual(updated_group_list.description, 'new_desc')
        self.assertFalse(updated_group_list.enable_chat)
        self.assertTrue(self.todo_list1 in updated_group_list.todos.all())

    def test_group_update_template_used(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(reverse('group_update', args=[self.group_list_1.id]))
        self.assertTemplateUsed(response, 'group_lists/group_update.html')

    # create

    def test_create_group_url(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.get('/group_lists/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_group_url_by_name(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.get(reverse('group_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_group_template_used(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.get(reverse('group_create'))
        self.assertTemplateUsed(response, 'group_lists/group_create.html')

    def test_create_group_functionality(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        post_credentials = {
            'title': 'new_group',
            'description': 'ng_desc',
            'enable_chat': ['on'],
            'todos': [self.reg_user_todo_list.id],
        }
        response = self.client.post(reverse('group_create'), post_credentials)
        new_group_list = GroupList.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(GroupList.objects.count(), 2)
        self.assertEqual(OnlineUsers.objects.count(), 1)
        self.assertEqual(new_group_list.title, 'new_group')
        self.assertEqual(new_group_list.description, 'ng_desc')
        self.assertTrue(new_group_list.enable_chat)
        self.assertTrue(self.reg_user_todo_list in new_group_list.todos.all())
        self.assertEqual(self.regularUser, new_group_list.admins.first())

    # detail
    def test_group_detail_url(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(f'/group_lists/{self.group_list_1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group_list_1.title.title())
        self.assertContains(response, self.group_list_1.get_invitation_link())
        self.assertContains(response, self.group_list_1.description)

    def test_group_detail_url_by_name(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(reverse('group_detail', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 200)

    def test_group_detail_shows_correct_members(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(reverse('group_detail', args=[self.group_list_1.id]))
        self.assertContains(response, self.ownerUser.username)
        self.assertContains(response, self.memberUser.username)
        self.assertContains(response, self.adminUser.username)

    def test_group_detail_shows_correct_todo_lists(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.get(reverse('group_detail', args=[self.group_list_1.id]))
        self.assertContains(response, self.todo_list1.name)

        # leave group

    def test_leave_group_denies_not_member_users(self):
        self.client.login(email=self.regularUserEmail, password=self.password)
        response = self.client.post(reverse('leave_group', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_leave_group_denies_owner_request(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.post(reverse('leave_group', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 403)

    def test_leave_group_functionality_with_admins(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.post(reverse('leave_group', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.adminUser2Email not in GroupList.objects.last().admins.all())

    def test_leave_group_functionality_with_members(self):
        self.client.login(email=self.memberUserEmail, password=self.password)
        response = self.client.post(reverse('leave_group', args=[self.group_list_1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.memberUserEmail not in GroupList.objects.last().members.all())

    # manage group users

    def test_manage_group_members_grade_denies_not_owner_request(self):
        self.client.login(email=self.adminUser2Email, password=self.password)
        response = self.client.post(reverse('manage_members_grade', args=[self.group_list_1.id]),
                                    {'': '', str(self.ownerUser.id): ''})
        self.assertEqual(response.status_code, 403)

    def test_manage_group_members_grade_denies_request_to_manage_owner(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.post(reverse('manage_members_grade', args=[self.group_list_1.id]),
                                    {'': '', str(self.ownerUser.id): ''})
        self.assertEqual(response.status_code, 403)

    def test_manage_group_members_grade_functionality_on_admins(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.post(reverse('manage_members_grade', args=[self.group_list_1.id]),
                                    {'': '', str(self.adminUser.id): ''})
        group = GroupList.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(group.is_member(self.adminUser))
        self.assertFalse(group.is_admin(self.adminUser))

    def test_manage_group_members_grade_functionality_on_members(self):
        self.client.login(email=self.ownerUserEmail, password=self.password)
        response = self.client.post(reverse('manage_members_grade', args=[self.group_list_1.id]),
                                    {'': '', str(self.memberUser.id): ''})
        group = GroupList.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(group.is_admin(self.adminUser))
        self.assertFalse(group.is_member(self.adminUser))
