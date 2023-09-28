import requests
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.views import BaseAPIView
from constants import constants
from utils import utils

from .models import Quiz
from .serializers import QuizSerializer


class QuizAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            now = utils.get_now_datetime()
            quiz = Quiz.objects.get(user=user, updated_at=now.date())
        except Exception as e:
            print(e)
            questions = utils.coin_get_questions()
            quiz = Quiz.objects.create(user=user, questions=questions)

        return Response(
            utils.get_response_data(
                data=QuizSerializer(quiz).data,
                success=1,
                message=constants.USER_DAILY_QUESTIONS,
            ),
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        answers = request.data.get("answers", {})
        user = request.user
        try:
            now = utils.get_now_datetime()
            quiz = Quiz.objects.get(user=user, updated_at=now.date())
        except Exception as e:
            print(e)
            questions = utils.coin_get_questions()
            quiz = Quiz.objects.create(user=user, questions=questions)

        questions = quiz.questions

        earned_coin = 0
        for question_index, answer in answers.items():
            if not answer:
                continue

            answer = str(answer)
            question = questions.get(question_index, {})
            if question and not question.get("answer", ""):
                question["answer"] = answer

                if question.get("correct_answer", "") == answer:
                    earned_coin += settings.COIN_PEER_TRUE_QUIZ
                    question["is_correct"] = True
                else:
                    earned_coin += settings.COIN_PEER_FALSE_QUIZ

                questions[question_index] = question

        quiz.questions = questions
        quiz.save()

        user.coin += earned_coin
        user.save()

        return Response(
            utils.get_response_data(
                data={
                    "earned_coin": earned_coin,
                    **QuizSerializer(quiz).data,
                },
                success=1,
                message=constants.ANSWER_SUCCESS,
            ),
            status=status.HTTP_201_CREATED,
        )
