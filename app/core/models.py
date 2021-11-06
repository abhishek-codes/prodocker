# from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
    BaseUserManager, PermissionsMixin
# from django.forms import fields
# from django.forms.fields import EmailField
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **args):
        """Creates ans Saves new User"""
        if phone is None:
            raise ValueError("User must enter Phone No")
        user = self.model(phone=phone, **args)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, phone, **args):
        """Create and save super user"""
        user = self.create_user(phone, **args)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user mode that user phone no intead of username"""
    phone = models.TextField(max_length=50, unique=True)
    name = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
