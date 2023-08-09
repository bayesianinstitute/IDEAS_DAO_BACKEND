from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_app.api.views import registration_view, CustomTokenObtainPairView,Forgotpassword


urlpatterns = [
  
    path('register/', registration_view, name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/forgotpassword/', Forgotpassword.as_view(), name='forgotpassword'),
]
