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
        try:
            data = super().validate(attrs)
            user = self.user

            user_data = User.objects.get(id=user.id)

            user_info = {
                'id': user_data.id,
                'username': user_data.username,
                'email': user_data.email
            }

            response_data = {
                'status': 'success',
                'data': user_info,
                'is_request_from_proxy': getattr(self.context['request'], 'is_request_from_proxy', False),
                'is_routable': getattr(self.context['request'], 'is_routable', True),
                'client_ip': getattr(self.context['request'], 'client_ip', ''),
            }
            response_data.update(data)  # Add the token data to the response_data

            return response_data

        except User.DoesNotExist:
            response_data = {
                'status': 'failure',
                'message': 'No active account found with the given credentials',
                'is_request_from_proxy': getattr(self.context['request'], 'is_request_from_proxy', False),
                'is_routable': getattr(self.context['request'], 'is_routable', True),
                'client_ip': getattr(self.context['request'], 'client_ip', ''),
            }
            return response_data
        except Exception as e:
            response_data = {
                'status': 'failure',
                'message': str(e) if str(e) else 'An error occurred.',
                'is_request_from_proxy': getattr(self.context['request'], 'is_request_from_proxy', False),
                'is_routable': getattr(self.context['request'], 'is_routable', True),
                'client_ip': getattr(self.context['request'], 'client_ip', ''),
            }
            return response_data


    
class OtpSerializer(serializers.Serializer):
    email = serializers.EmailField()