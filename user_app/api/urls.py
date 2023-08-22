from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_app.api.views import registration_view, CustomTokenObtainPairView,sent_otp, ResetPassword,confirm_registration


urlpatterns = [
  
    path('api/register/', registration_view, name='register'),
    path('confirm/<int:user_id>/', confirm_registration, name='confirm_registration'),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/sent/otp', sent_otp.as_view(), name='forgotpassword'),
    path('api/reset_password/', ResetPassword.as_view(), name='reset-password'),
    
]
