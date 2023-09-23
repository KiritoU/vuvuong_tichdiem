from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from constants import constants
from utils import utils

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=45)
    device_id = serializers.CharField(max_length=80)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "device_id", "password", "inviter_code"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        if email:
            email_exists = User.objects.filter(
                email=email, is_validated_email=True
            ).exists()

            if email_exists:
                raise ValidationError(constants.EMAIL_EXIST)

        username_exists = User.objects.filter(username=attrs["username"]).exists()

        if username_exists:
            raise ValidationError(constants.USERNAME_EXIST)

        device_id_exists = User.objects.filter(device_id=attrs["device_id"]).exists()

        if device_id_exists:
            raise ValidationError(constants.DEVICE_EXIST)

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        invitation_code = utils.generate_invation_code()
        while User.objects.filter(invitation_code=invitation_code).exists():
            invitation_code = utils.generate_invation_code()

        user.invitation_code = invitation_code
        user.save()

        inviter_code = validated_data.get("inviter_code", "")
        if inviter_code:
            inviter = User.objects.filter(invitation_code=inviter_code)
            if inviter.exists():
                inviter = inviter.first()
                inviter.receive_invitation_reward()
                user.receive_invitation_reward()

        Token.objects.create(user=user)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "invitation_code", "coin", "is_validated_email"]
