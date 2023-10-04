import calendar
import random
import string
from datetime import datetime

import pytz
import requests
from django.conf import settings
from django.utils import timezone


class Utils:
    def get_response_data(self, data, success: int, message: str) -> dict:
        return {
            "success": success,
            "message": message,
            "data": data,
        }

    def generate_invation_code(self, code_length: int = 6) -> str:
        letters_and_digits = string.ascii_letters + string.digits

        return "".join(
            random.choice(letters_and_digits) for i in range(code_length)
        ).upper()

    def get_now_datetime(self):
        now = timezone.localtime(
            timezone.now(), timezone=pytz.timezone(settings.TIME_ZONE)
        )

        return now

    def coin_get_questions(self):
        questions = {}

        try:
            response = requests.get(settings.QUIZ_URL, timeout=20)
            results = response.json().get("results", [])

            for i, result in enumerate(results):
                questions[i] = {
                    **result,
                    "answer": "",
                    "is_correct": False,
                }

        except Exception as e:
            print(e)

        return questions

    def get_days_response(self, checked_in_data: list) -> dict:
        now = self.get_now_datetime()

        days_in_month = calendar.monthrange(now.year, now.month)[1]
        days = {
            f"{day}-{now.month}-{now.year}": False
            for day in range(1, days_in_month + 1)
        }

        for day in checked_in_data:
            days[day.strip("0")] = True

        return days


utils = Utils()
