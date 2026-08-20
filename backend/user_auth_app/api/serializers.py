from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile
from django.contrib.auth import authenticate
import re


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = []


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except user.DoesNotExist:
            raise serializers.ValidationError("Email does not exist")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Password not correct")

        data["user"] = user
        data["fullname"] = user.userprofile.fullname
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile

        fields = ["fullname", "email", "password", "repeated_password"]

    def save(self):
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]
        pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        
        if pw != repeated_pw:
            raise serializers.ValidationError({"error": "passwords dont match"})

        if UserProfile.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError("Email already exists")

        if not re.match(pattern, self.validated_data["email"]):
             raise serializers.ValidationError("Invalid email format")
         
        account = User(
        username=self.validated_data["email"],
        email=self.validated_data["email"],
    )
        account.set_password(pw)
        account.save()
    
        UserProfile.objects.create(
            user=account,
            email=self.validated_data["email"],
            fullname=self.validated_data["fullname"],
        )
    
        return account
