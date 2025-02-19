import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from fatcode import settings
from src.base.validators import ImageValidator
from src.courses.models import Course
from .validators import phone_validator


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


class Invitation(models.Model):
    """Модель приглашений"""
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.code


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
    reputation = models.IntegerField(default=0)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    coins = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    USERNAME_FIELD = "username"


class FatUserSocial(models.Model):
    """Intermediate table for the ManyToMany FatUser and Social relationship"""
    social = models.ForeignKey(Social, on_delete=models.CASCADE, related_name='link_social')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_social'
    )
    user_url = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.user_url


class Account(models.Model):
    """Модель аккаунтов привязанных к пользователю"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_account'
    )
    provider = models.CharField(max_length=25, default='')
    account_id = models.CharField(max_length=150, blank=True, null=True)
    account_url = models.CharField(max_length=250, default='')
    account_name = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.account_url


class Language(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    """Модель анкеты"""
    description = models.TextField()
    country = models.CharField(max_length=150, blank=True, null=True)
    town = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(validators=[phone_validator], max_length=13, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='questionnaire/avatar/',
        default='default/default.jpg',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg']),
            ImageValidator((250, 250), 524288)
        ]
    )
    user = models.OneToOneField(FatUser, on_delete=models.CASCADE, related_name='questionnaire')
    toolkits = models.ManyToManyField(
        'repository.Toolkit',
        related_name="questionnaire_projects",
        blank=True
    )
    teams = models.ManyToManyField('team.Team', related_name='questionnaire_teams', blank=True)
    projects = models.ManyToManyField(
        'repository.Project',
        related_name='questionnaire_projects',
        blank=True
    )
    accounts = models.ManyToManyField(Account, related_name='questionnaire_accounts', blank=True)
    languages = models.ManyToManyField(Language, related_name="questionnaire_language", blank=True)
    socials = models.ManyToManyField(FatUserSocial, related_name="questionnaire_social", blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


class Application(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender"
    )
    getter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="getter"
    )

    def __str__(self):
        return f'{self.sender} wants to be friends with {self.getter}'


class Friend(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user"
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friend"
    )

    def __str__(self):
        return f'{self.friend} is friends with {self.user}'


