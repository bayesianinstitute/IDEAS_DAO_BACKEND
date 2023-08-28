from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ideasApi.models import Device,Member,Delegate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password  # Import the password verifier

from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Member
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        """
        Custom validation to check if the passwords match.
        """
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def validate_email(self, value):
        """
        Custom validation for email uniqueness.
        """
        if Member.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value

    def save(self, **kwargs):
        password = self.validated_data["password"]
        email = self.validated_data["email"]
        username = self.validated_data["username"]

        account = Member(username=username, email=email, password=make_password(password))
        account.save()

        return account


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        member = Member.objects.filter(username=username).first()

        if member and check_password(password, member.password):
            refresh = RefreshToken.for_user(member)
            data = {
                'status': 'success',
                'data': [
                    {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                    }
                ],
                'message': 'Request successful.',
                'is_request_from_proxy': False,
                'is_routable': True,
                'client_ip': self.context['request'].META.get('REMOTE_ADDR', ''),
            }
            return data

        data = {
            'status': 'failure',
            'message': 'Invalid credentials.',
            'is_request_from_proxy': False,
            'is_routable': True,
            'client_ip': self.context['request'].META.get('REMOTE_ADDR', ''),
        }
        return data

        
class OtpSerializer(serializers.Serializer):
    email = serializers.EmailField()