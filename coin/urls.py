from django.urls import path

from .views import (
    QuizAPIView,
    UserCodeWithCoinAPIView,
    UserMonthlyCheckinRewardAPIView,
    UserRotateLuckAPIView,
)

urlpatterns = [
    path("quiz/", QuizAPIView.as_view(), name="coin-quiz"),
    path("checkin/", UserMonthlyCheckinRewardAPIView.as_view(), name="coin-checkin"),
    path("code/", UserCodeWithCoinAPIView.as_view(), name="coin-code"),
    path("rotation/", UserRotateLuckAPIView.as_view(), name="coin-rotation"),
]
