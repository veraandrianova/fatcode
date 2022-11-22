import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from fatcode import settings
from src.base.validators import ImageValidator
from src.courses.models import Course


def user_directory_path(instance: 'FatUser', filename: str) -> str:
    """Generate path to file in upload"""
    return f'users/avatar/user_{instance.id}/{str(uuid.uuid4())}.{filename.split(".")[-1]}'


class Social(models.Model):
    """Social networks"""
    title = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to='social/logo',
        null=True,
        blank=True,
        validators=[ImageValidator((50, 50), 524288)]
    )
    url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class FatUser(AbstractUser):
    """User model override"""
    avatar = models.ImageField(
        upload_to=user_directory_path,
        default='default/default.jpg',
        null=True,
        blank=True,
        validators=[ImageValidator((100, 100), 1048576)]
    )
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    socials = models.ManyToManyField(Social, through='FatUserSocial')
    experience = models.IntegerField(default=0)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    coins = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    USERNAME_FIELD = "username"


class FatUserSocial(models.Model):
    """Intermediate table for the ManyToMany FatUser and Social relationship"""
    social = models.ForeignKey(Social, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_social'
    )
    user_url = models.CharField(max_length=500, default='')


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_account')
    provider = models.CharField(max_length=25, default='')
    account_id = models.CharField(max_length=150, blank=True, null=True)
    account_url = models.CharField(max_length=250, default='')
    account_name = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.account_id


class Applications(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    getter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="getter")

    def __str__(self):
        return f'{self.sender} wants to be friends with {self.getter}'


class Friends(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend")

    def __str__(self):
        return f'{self.friend} is friends with {self.user}'
