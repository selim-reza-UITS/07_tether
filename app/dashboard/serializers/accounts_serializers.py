from django.contrib.auth import authenticate
from rest_framework import serializers

from app.accounts.models import User, UserProfile


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_staff:
            raise serializers.ValidationError("You do not have admin access.")

        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['image', 'address', 'age', 'status']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfile
    # profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'profile']