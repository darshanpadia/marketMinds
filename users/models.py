from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import requests
import json

from .managers import CustomUserManager
# To make email primary field for user. Username field removed.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        default="https://res.cloudinary.com/dsu3jrywn/image/upload/v1742366111/blank-profile_ye4tm3.jpg"
    )

    image_url = models.URLField(_('image URL'), blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    REQUIRED_FIELDS = [] 
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def __str__(self):
        return self.email

    def save(self, **kwargs):
        super().save(**kwargs)


