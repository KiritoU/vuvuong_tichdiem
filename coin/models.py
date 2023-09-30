from django.db import models

from accounts.models import User


def get_empty_string():
    return ""


class Code(models.Model):
    code = models.CharField(max_length=25)
    name = models.CharField(
        max_length=255, blank=True, null=True, default=get_empty_string
    )
    coin_price = models.PositiveIntegerField(default=1000, blank=True, null=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="codes"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.code

    class Meta:
        ordering = ("-updated_at",)


class Quiz(models.Model):
    user = models.ForeignKey(User, related_name="quiz", on_delete=models.CASCADE)
    questions = models.JSONField()
    updated_at = models.DateField(auto_now=True)


class RotationLuckReward(models.Model):
    code_with_coin_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    coin = models.PositiveIntegerField(default=0, blank=True, null=True)
    rate = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("rate",)


class MonthlyCheckinReward(models.Model):
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    day_count = models.PositiveIntegerField()
    coin = models.PositiveIntegerField(default=0)

    users = models.ManyToManyField(
        User, related_name="monthlycheckinrewards", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.day_count} of {self.month}/{self.year} => {self.coin} coin(s)"
