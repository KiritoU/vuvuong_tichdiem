from django.urls import path

from .views import QuizAPIView

urlpatterns = [
    path("quiz/", QuizAPIView.as_view(), name="coin-quiz"),
]
