# from typing import ValuesView
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_phone_successful(self):
        """Test creating a new user with an email is successful"""
        phone = "+919999999999"
        user = get_user_model().objects.create_user(
            phone=phone
        )
        self.assertEqual(user.phone, phone)

    # def test_new_user_phone_normalised(self):
    #     """Test phone for new user is normalised"""
    #     phone = "+919595955666"
    #     user = get_user_model().objects.create_user(phone)
    #     self.assertEqual(user.phone, phone)

    def test_new_user_invalid_phone(self):
        """Test creating user with no phone raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None)

    def test_create_new_super_user(self):
        """Test new super user created"""
        user = get_user_model().objects.create_superuser('+919999999999')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
