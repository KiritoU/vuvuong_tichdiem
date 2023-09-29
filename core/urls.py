from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(f"{settings.DJANGO_ADMIN_URL}/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("coin/", include("coin.urls")),
]
