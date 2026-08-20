from django.urls import path
from .views import UserProfileList, RegistrationView, CustomLogin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLogin.as_view(), name='login'),
]