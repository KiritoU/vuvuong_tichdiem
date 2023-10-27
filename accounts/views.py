from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.utils import timezone
from icecream import ic
from rest_framework import generics, status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from constants import constants
from utils import utils

from .models import Checkin, History, User
from .serializers import HistorySerializer, SignUpSerializer, UserInfoSerializer
from .tokens import create_jwt_pair_for_user

# Create your views here.


class BaseAPIView(APIView):
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                utils.get_response_data(
                    data=[],
                    success=0,
                    message=constants.PERMISSION_DENIED,
                ),
                status=status.HTTP_403_FORBIDDEN,
            )
        elif isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            return Response(
                utils.get_response_data(
                    data=[],
                    success=0,
                    message=constants.UNAUTHORIZED,
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().handle_exception(exc)


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = utils.decrypt_request(request.data)
        if not data:
            return Response(
                utils.get_response_data(
                    data=[], success=0, message=constants.DATA_ERROR
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()
            tokens = create_jwt_pair_for_user(user)

            return Response(
                utils.get_response_data(
                    data={**tokens, **UserInfoSerializer(user).data},
                    success=1,
                    message=constants.SIGNUP_SUCCESS,
                ),
                status=status.HTTP_201_CREATED,
            )

        return Response(
            utils.get_response_data(
                data=[], success=0, message=serializer.errors["errors"][0]
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(BaseAPIView):
    permission_classes = []

    def post(self, request):
        request_data = utils.decrypt_request(request.data)

        username = request_data.get("username")
        password = request_data.get("password")
        device_id = request_data.get("device_id")

        user = authenticate(username=username, password=password)
        if user and user.device_id == device_id:
            tokens = create_jwt_pair_for_user(user)

            return Response(
                utils.get_response_data(
                    data={**tokens, **UserInfoSerializer(user).data},
                    success=1,
                    message=constants.LOGIN_SUCCESS,
                ),
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                utils.get_response_data(
                    data=[], success=0, message=constants.LOGIN_FAILED
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserInfoView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get(self, request: Request):
        try:
            return Response(
                utils.get_response_data(
                    data=self.serializer_class(request.user).data,
                    success=1,
                    message=constants.USER_INFO,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                utils.get_response_data(
                    data=[],
                    success=0,
                    message=constants.USER_INFO_FAILED,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserCheckinAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        now = utils.get_now_datetime()
        user_checkins = request.user.checkins.filter(date__month=now.month)
        data = [checkin.__str__() for checkin in user_checkins]

        days = utils.get_days_response(checked_in_data=data)

        return Response(
            utils.get_response_data(
                data=days,
                success=1,
                message=constants.USER_CHECKIN,
            ),
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        now = utils.get_now_datetime()
        today_checkin, _ = Checkin.objects.get_or_create(date=now.date())
        is_user_checked_in = today_checkin.users.filter(
            username=request.user.username
        ).exists()

        data = [
            checkin.__str__()
            for checkin in request.user.checkins.filter(date__month=now.month)
        ]

        days = utils.get_days_response(checked_in_data=data)

        if is_user_checked_in:
            return Response(
                utils.get_response_data(
                    data={
                        "earned_coin": 0,
                        "days": days,
                    },
                    success=0,
                    message=constants.USER_ALREADY_CHECKED_IN,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.coin += settings.COIN_PEER_DAILY_CHECKIN
        request.user.save()
        today_checkin.users.add(request.user)
        data = [
            checkin.__str__()
            for checkin in request.user.checkins.filter(date__month=now.month)
        ]
        days = utils.get_days_response(checked_in_data=data)

        return Response(
            utils.get_response_data(
                data={
                    "earned_coin": settings.COIN_PEER_DAILY_CHECKIN,
                    "days": days,
                },
                success=1,
                message=constants.USER_CHECKIN_SUCCESS,
            ),
            status=status.HTTP_200_OK,
        )


class UserHistoryListAPIView(BaseAPIView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerializer

    def get_queryset(self):
        queryset = History.objects.filter(user=self.request.user)

        history_type = self.request.query_params.get("type", "")
        if history_type:
            queryset = queryset.filter(type=history_type)

        return queryset
