from django.urls import path

from .views import UserCreateApiView

app_name = "accounts_api"

urlpatterns = [
    path("user/", view=UserCreateApiView.as_view(), name="create_user"),
]
