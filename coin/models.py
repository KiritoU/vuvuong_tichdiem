from django.db import models

from accounts.models import User


class Quiz(models.Model):
    user = models.ForeignKey(User, related_name="quiz", on_delete=models.CASCADE)
    questions = models.JSONField()
    updated_at = models.DateField(auto_now=True)
