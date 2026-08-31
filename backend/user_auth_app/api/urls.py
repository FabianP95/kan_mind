"""Authentication API endpoints for registration, login, and email checks."""

from django.urls import path

from .views import RegistrationView, CustomLogin, CheckEmailView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", CustomLogin.as_view(), name="login"),
    path("email-check/", CheckEmailView.as_view(), name="email-check"),
]
