from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_app.models import (
       Profile
)

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """
        Custom validation for email uniqueness.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value

    def save(self, **kwargs):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"error": "P1 and P2 should be the same!"})

        email = self.validated_data["email"]
        username = self.validated_data["username"]

        account = User.objects.create_user(username=username, email=email, password=password)

        return account

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_valid']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        data.update({'user': user_data})
        data['is_request_from_proxy'] = getattr(self.context['request'], 'is_request_from_proxy', False)
        data['is_routable'] = getattr(self.context['request'], 'is_routable', True)
        data['client_ip'] = getattr(self.context['request'], 'client_ip', '')

        return data
    
class OtpSerializer(serializers.Serializer):
    email = serializers.EmailField()