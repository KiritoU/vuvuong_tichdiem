from rest_framework import serializers

from .models import Code, Quiz, RotationLuckReward


class QuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = "__all__"

    def get_questions(self, quiz: Quiz) -> dict:
        res = {}

        for k, v in quiz.questions.items():
            del v["correct_answer"]
            del v["incorrect_answers"]

            res[k] = v

        return res


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ["code", "name", "coin_price"]


class RotationLuckRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotationLuckReward
        fields = ["code_with_coin_price", "coin", "rate"]
