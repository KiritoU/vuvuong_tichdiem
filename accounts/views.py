from django.contrib.auth import authenticate
from django.shortcuts import render
from django.utils import timezone
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

from .models import Checkin, User
from .serializers import SignUpSerializer, UserInfoSerializer
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
        data = request.data

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


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")
        device_id = request.data.get("device_id")

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
                    data=tokens, success=1, message=constants.LOGIN_FAILED
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
        now = timezone.now()
        user_checkins = request.user.checkins.filter(date__month=now.month)
        data = [checkin.__str__() for checkin in user_checkins]

        return Response(
            utils.get_response_data(
                data=data,
                success=1,
                message=constants.USER_CHECKIN,
            ),
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        today_checkin, _ = Checkin.objects.get_or_create(date=now.date())
        is_user_checked_in = today_checkin.users.filter(
            username=request.user.username
        ).exists()

        data = [checkin.__str__() for checkin in request.user.checkins.all()]

        if is_user_checked_in:
            return Response(
                utils.get_response_data(
                    data=data,
                    success=0,
                    message=constants.USER_ALREADY_CHECKED_IN,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        today_checkin.users.add(request.user)

        return Response(
            utils.get_response_data(
                data=data,
                success=1,
                message=constants.USER_CHECKIN_SUCCESS,
            ),
            status=status.HTTP_200_OK,
        )
