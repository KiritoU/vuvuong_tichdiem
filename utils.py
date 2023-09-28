import random
import string

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
            response = requests.get(settings.QUIZ_URL)
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


utils = Utils()
