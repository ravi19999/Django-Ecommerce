from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.core.mail import send_mail
from django.template.loader import get_template


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, active=True, is_active=True, password=None, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        # if not full_name:
        #     raise ValueError("Users must have a full name")
        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = True
        user_obj.active = True
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,  email,  password=None, full_name=None):
        user = self.create_user(
            email, full_name=full_name, password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email,  password=None, full_name=None):
        user = self.create_user(
            email,
            full_name=full_name, password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @ property
    def is_staff(self):
        return self.staff

    @ property
    def is_admin(self):
        return self.admin

    # @ property
    # def is_active(self):
    #     return self.active


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
