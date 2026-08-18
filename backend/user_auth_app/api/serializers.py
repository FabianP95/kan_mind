from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["email", "password"]


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email does not exist")

        user = authenticate(password=password)

        if user is None:
            raise serializers.ValidationError("Password not correct")

        data["user"] = user
        return data


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = ["username", "email", "password", "repeated_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]

        if pw != repeated_pw:
            raise serializers.ValidationError({"error": "passwords dont match"})

        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError("Email already exists")

        account = User(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        account.set_password(pw)
        account.save()
        return account
