from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            phone='+919898989898'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            phone='+919999999999',
            name='Test user'
        )

    def test_users_listed(self):
        """Test users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        # print(res)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.phone)

    def test_user_change_page(self):
        """Test user edit page works"""
        url = reverse('admin:core_user_change', args={self.user.id})
        # /admin/core/user/id
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test That create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
