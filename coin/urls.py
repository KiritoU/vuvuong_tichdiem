from django.urls import path

from .views import QuizAPIView, UserCodeWithCoinAPIView, UserRotateLuckAPIView

urlpatterns = [
    path("quiz/", QuizAPIView.as_view(), name="coin-quiz"),
    path("code/", UserCodeWithCoinAPIView.as_view(), name="coin-code"),
    path("rotation/", UserRotateLuckAPIView.as_view(), name="coin-rotation"),
]
