from unittest import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.utils import IntegrityError

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Hepler function to create user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_user_valid_user_success(self):
        """Test for valid user created"""
        payload = {
            'phone': '+917272727222',
            'name': 'name',
            'password': 'Test@1234'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_exists_fails(self):
        """Test user exists and fails"""
        payload = {
            'phone': '+917272727134',
            'name': 'name',
            'password': 'Test@1234'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test a new token is created"""
        payload = {
            'phone': '+917272727213',
            'name': 'name',
            'password': 'Test@1234'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Test invalid credentials"""
        payload = {
            'phone': '+917272727111',
            'name': 'name',
            'password': 'Test@1234'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test invalid User"""
        payload = {
            'phone': '+91727272112',
            'name': 'name',
            'password': 'Test@1234'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test Blank Fields"""
        res = self.client.post(TOKEN_URL, {'phone': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorised(self):
        """Test Authentication is required for user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test User API (private) require Authentication"""

    def setUp(self):
        try:
            self.user = create_user(
                phone='+9172727298', name='test', password='Test@1234')
        except IntegrityError:
            self.user = get_user_model().objects.get(phone='+9172727298')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_user_authorised(self):
        """Test Retriving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({
            'name': self.user.name,
            'phone': self.user.phone
        }, res.data)

    def test_post_me_not_allowed(self):
        """Test post not allowed"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test update is Allowed for Authenticated User"""
        payload = {'name': 'testUpdate', 'password': 'Update@1234'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
