from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

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
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value

    def save(self, **kwargs):
        password = self.validated_data["password"]
        email = self.validated_data["email"]
        username = self.validated_data["username"]

        account = User.objects.create_user(username=username, email=email, password=password)

        return account

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user

        try:
            user_data = User.objects.get(id=user.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        user_info = {
            'id': user_data.id,
            'username': user_data.username,
            'email': user_data.email
        }

        data.update({'user': user_info})
        data['is_request_from_proxy'] = getattr(self.context['request'], 'is_request_from_proxy', False)
        data['is_routable'] = getattr(self.context['request'], 'is_routable', True)
        data['client_ip'] = getattr(self.context['request'], 'client_ip', '')

        return data
    
class OtpSerializer(serializers.Serializer):
    email = serializers.EmailField()