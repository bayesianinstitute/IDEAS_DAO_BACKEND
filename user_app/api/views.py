from user_app.api.serializers import CustomTokenObtainPairSerializer, RegistrationSerializer, OtpSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.mail import send_mail
from rest_framework.views import APIView
import requests
import json
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from ideasApi.api.models import (
       Otp
)

    
@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Check if all required fields are present in the request
            required_fields = ['username', 'password', 'email']
            if all(key in request.data for key in required_fields):
                account = serializer.save()
                data = {
                    'response': 'Registration Successful!',
                    'username': account.username,
                    'email': account.email,
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = {'error': 'All required fields are not present in the request'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# class CustomObtainAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == status.HTTP_400_BAD_REQUEST:
#             return Response({
#                 "error": "Unable to log in with provided credential."
#             }, status=status.HTTP_400_BAD_REQUEST)
#         return 

class Forgotpassword(APIView):
    def post(self, request, format=None):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if an OTP entry already exists for the user
            user = User.objects.filter(email=email).first()
            if user:
                otp_instance = Otp.objects.filter(user=user).first()
                if otp_instance:
                    # Update the existing OTP instance
                    otp_instance.otp_value = random.randint(1000, 9999)
                    otp_instance.expiry_time = datetime.now() + timedelta(minutes=15)
                    otp_instance.save()
                else:
                    # Create a new OTP instance
                    otp = random.randint(1000, 9999)
                    expiry_time = datetime.now() + timedelta(minutes=15)
                    otp_instance = Otp.objects.create(user=user, expiry_time=expiry_time, otp_value=otp)
            else:
                # Create a new user and OTP instance
                user = User.objects.create(email=email)
                otp = random.randint(1000, 9999)
                expiry_time = datetime.now() + timedelta(minutes=15)
                otp_instance = Otp.objects.create(user=user, expiry_time=expiry_time, otp_value=otp)
            
            # Send OTP to the provided email
            send_mail(
                'Your OTP',
                f'Your OTP is: {otp_instance.otp_value}',
                'bayesdev2@gmail.com',  # Replace with your sender email
                [email],
                fail_silently=False,
            )
            
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
