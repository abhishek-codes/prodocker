from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
    BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
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
    phRex = RegexValidator(
        r'^\+[1-9]{1}[0-9]{7,16}$', message="Phone number must be entered in the \
        format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phRex], max_length=20, unique=True)
    name = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
