import json
import datetime

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_user(self, phone, password, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(
            phone=phone,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields)

        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, phone, password, is_staff=True, is_superuser=True, **extra_fields):
        return self.create_user(phone=phone, password=password, is_staff=is_staff, is_superuser=is_superuser,
                                **extra_fields)


class User(AbstractUser):
    fio = models.CharField(_("Ism familiya"), max_length=50)
    phone = models.CharField(_("Telefon raqam"), max_length=50, unique=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.SmallIntegerField(default=1, choices=[
        (1, 'user'),
        (2, 'admin')
    ])

    username = False
    email = False
    first_name = False
    last_name = False

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['user_type']


class OTP(models.Model):
    key = models.CharField('TOKEN', max_length=256, unique=True, primary_key=True)
    mobile = models.CharField(max_length=15)

    is_expired = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)
    extra = models.JSONField(default=json.dumps({}))
    is_verified = models.BooleanField(default=False)

    step = models.CharField(
        max_length=256,
        choices=[
            ('regis', 'Registration'),
            ('send', 'OTP send'),
            ('conf_regis', 'Registered'),
            ('login', 'Login'),
            ('send_login', 'OTP send'),
            ('conf_login', 'Logged in'),
        ]
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tries >= 3 or self.is_verified:
            self.is_expired = True
        return super().save(*args, **kwargs)

    def check_expire_date(self):
        now = datetime.datetime.now()
        if (now - self.created).total_seconds() >= 60:
            self.is_expired = True
            self.save()
            return False
        return True
