from django.urls import path
from .views import RegistrationView, CustomLogin, CheckEmailView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", CustomLogin.as_view(), name="login"),
    path("email-check/", CheckEmailView.as_view(), name="email-check"),
]
