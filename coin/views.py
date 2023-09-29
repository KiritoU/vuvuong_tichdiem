import random

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.views import BaseAPIView
from constants import constants
from utils import utils

from .models import Code, Quiz, RotationLuckReward
from .serializers import CodeSerializer, QuizSerializer, RotationLuckRewardSerializer


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
            answer = str(answer)
            if not answer:
                continue

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
        # TODO: Noti / history

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


class UserCodeWithCoinAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        codes = request.user.codes.all()  # TODO: Change to list or limit the output

        return Response(
            utils.get_response_data(
                data=CodeSerializer(codes, many=True).data,
                success=1,
                message=constants.USER_LIST_CODES,
            ),
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        coin_price = request.data.get("coin_price", 0)

        if coin_price <= 0:
            return Response(
                utils.get_response_data(
                    data=[],
                    success=0,
                    message=constants.COIN_PRICE_LTE_ZERO,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        codes = Code.objects.filter(user__isnull=True)
        if not codes.exists():
            return Response(
                utils.get_response_data(
                    data=[],
                    success=0,
                    message=constants.CODE_WITH_COIN_PRICE_DOES_NOT_EXIST.format(
                        coin_price
                    ),
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        code = codes.last()
        code.user = user
        code.save()
        # TODO: Noti / history

        return Response(
            utils.get_response_data(
                data=CodeSerializer(code).data,
                success=1,
                message=constants.USER_EXCHANGE_CODE_SUCCESS,
            ),
            status=status.HTTP_200_OK,
        )


class UserRotateLuckAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rewards = RotationLuckReward.objects.all()
        return Response(
            utils.get_response_data(
                data={
                    "rotate_price": settings.ROTATE_COIN_PRICE,
                    "rewards": RotationLuckRewardSerializer(rewards, many=True).data,
                },
                success=1,
                message=constants.USER_LIST_ROTATION_LUCK_REWARDS,
            ),
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.coin < settings.ROTATE_COIN_PRICE:
            return Response(
                utils.get_response_data(
                    data=[],
                    success=0,
                    message=constants.NOT_ENOUGH_COIN,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        rewards = RotationLuckReward.objects.all()

        sum_rate = sum([reward.rate for reward in rewards])
        print(f"sum_rate: {sum_rate}")

        picked_number = random.randint(1, sum_rate)
        print(f"picked_number: {picked_number}")

        start = 0
        for reward in rewards:
            if start < picked_number <= start + reward.rate:
                is_reward_code_still_exist = True
                if reward.code_with_coin_price > 0:
                    code = Code.objects.get(
                        user__isnull=True, coin_price=reward.code_with_coin_price
                    )
                    code.user = user
                    code.save()
                    is_reward_code_still_exist = Code.objects.filter(
                        user__isnull=True, coin_price=reward.code_with_coin_price
                    ).exists()

                user.coin += reward.coin

                response = utils.get_response_data(
                    data=RotationLuckRewardSerializer(reward).data,
                    success=1,
                    message=constants.USER_ROTATE_SUCCESS,
                )

                if not is_reward_code_still_exist:
                    reward.delete()

                user.coin -= settings.ROTATE_COIN_PRICE
                user.save()

                return Response(response, status=status.HTTP_200_OK)

            start += reward.rate
