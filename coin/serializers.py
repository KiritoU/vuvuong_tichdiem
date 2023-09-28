from rest_framework import serializers

from .models import Quiz


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
