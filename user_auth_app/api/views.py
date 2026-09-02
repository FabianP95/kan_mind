"""Authentication endpoints for login, registration, and email lookup."""

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

from .serializers import UserLoginSerializer, RegistrationSerializer


class CustomLogin(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "fullname": serializer.validated_data["fullname"],
                "email": user.email,
                "user_id": user.id,
            }
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()

            data = {"username": saved_account.username, "email": saved_account.email}
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


class CheckEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email")

        if not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            data = {
                "id": user.id,
                "email": user.email,
                "fullname": user.userprofile.fullname,
            }
            return Response(data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
