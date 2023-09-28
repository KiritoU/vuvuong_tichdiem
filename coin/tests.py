import pytz
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from utils import utils

from .models import Quiz


class QuizTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="test",
            device_id="TEST",
            password="QWER1234!@#$",
        )

        questions = utils.coin_get_questions()
        Quiz.objects.create(user=user, questions=questions)

    def test_user_has_daily_quiz(self):
        user = User.objects.get(username="test")
        quiz = user.quiz.first()

        now = utils.get_now_datetime()

        quiz = user.quiz.filter(updated_at=now.date())

        self.assertEqual(quiz.exists(), True)
