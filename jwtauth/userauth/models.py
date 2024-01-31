from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import ProfileManager

# Create your models here.


class TimeStamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(AbstractBaseUser, PermissionsMixin, TimeStamp):

    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ProfileManager()

    class Meta:
        verbose_name = "User"


class Otp(TimeStamp):

    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    otp_data = models.IntegerField(null=False)
