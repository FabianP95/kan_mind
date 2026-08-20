from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status


class UserProfileList(generics.ListCreateAPIView):
    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


class CustomLogin(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'fullname': serializer.validated_data['fullname'],
                'email': user.email,
                'user_id': user.id,
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
            
            data = {
                
                'username':saved_account.username,
                'email': saved_account.email
            }
        else:
            data = serializer.errors
            
        return Response(data, status=status.HTTP_201_CREATED)