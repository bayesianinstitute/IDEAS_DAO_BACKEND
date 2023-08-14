from user_app.api.serializers import CustomTokenObtainPairSerializer, RegistrationSerializer, OtpSerializer,ProfileSerializer
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
from django.views.decorators.csrf import csrf_protect
from ideasApi.models import (
       Otp
)
from user_app.models import (
       Profile
)

    
@api_view(['POST'])

def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email']
            )

            # Create a corresponding Profile instance with is_valid set to False
            profile = Profile.objects.create(
                name=user.username,  # You can customize how you want to set the name
                Django_user=user,
                is_valid=False
            )

            profile_serializer = ProfileSerializer(profile)  # Assuming you have a serializer for the Profile model
            data = {
                'response': 'Registration Successful!',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'is_valid': profile.is_valid
                },
                
            }
            return Response(data, status=status.HTTP_201_CREATED)
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
            
            # Check if the user exists in the database
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'message': 'User not registered with this email'}, status=status.HTTP_400_BAD_REQUEST)
            
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
    
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_otp_view(request):
    if request.method == "POST":
        email = request.data.get("email")
        otp_value = request.data.get("otp_value")
        data = {}
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            data["error"] = "User not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            otp_obj = Otp.objects.get(user=user)
        except Otp.DoesNotExist:
            data["error"] = "OTP not generated for this user"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if otp_obj.expiry_time <= timezone.now():
            # OTP has expired
            data["error"] = "OTP has expired"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.otp_value == otp_value:
            # OTP is valid
            # otp_obj.delete()
            try:
                profile = Profile.objects.get(Django_user=user)
                if profile.is_valid:
                    data["response"] = "OTP verification was done previously"
                    return Response(data, status=status.HTTP_200_OK)
                profile.is_valid = True  # Set is_valid flag to True
                profile.save()  # Save the changes
                data["response"] = "OTP verification successful"
                return Response(data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                data["error"] = "Profile not found"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            # OTP is invalid
            data["error"] = "Invalid OTP"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

    
    