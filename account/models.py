from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, name, password=None):

        if not username:
            raise ValueError('Username not provided')

        user = self.model(username=username, name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, name, password):

        user = self.create_user(username, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name',]

    objects = UserProfileManager()

    def __str__(self):
        return self.username