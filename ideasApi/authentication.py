from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from ideasApi.models import Member

class MemberJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token[api_settings.USER_ID_CLAIM]
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None

class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and isinstance(user, Member))