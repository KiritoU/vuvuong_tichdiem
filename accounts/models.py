from datetime import datetime

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from constants import constants


def get_empty_string():
    return ""


class CustomUserManager(BaseUserManager):
    def create_user(self, password, **extra_fields):
        extra_fields["email"] = self.normalize_email(extra_fields.get("email", ""))

        user = self.model(**extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields["email"] = self.normalize_email(extra_fields.get("email", ""))

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(password=password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=45, unique=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    device_id = models.CharField(max_length=80, unique=True)
    invitation_code = models.CharField(max_length=80, blank=True, null=True)
    inviter_code = models.CharField(max_length=80, blank=True, null=True)

    is_validated_email = models.BooleanField(default=False)
    coin = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["device_id"]

    def __str__(self):
        return self.username

    def receive_invitation_reward(self):
        self.coin += settings.COIN_PEER_INVITATION
        self.histories.create(
            type="COIN",
            coin=settings.COIN_PEER_INVITATION,
            content=constants.HISTORY_RECEIVE_INVITATION_REWARD,
        )
        self.save()


class Checkin(models.Model):
    date = models.DateField()
    users = models.ManyToManyField(User, related_name="checkins")

    def __str__(self) -> str:
        return self.date.strftime("%d-%m-%Y")

    class Meta:
        ordering = ("-date",)


class History(models.Model):
    TYPE_CHOICES = (
        ("COIN", "COIN"),
        ("CODE", "CODE"),
    )

    user = models.ForeignKey(
        User, related_name="histories", on_delete=models.CASCADE, db_index=True
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="COIN")
    coin = models.IntegerField(default=0)
    content = models.CharField(
        max_length=255, blank=True, null=True, default=get_empty_string
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
