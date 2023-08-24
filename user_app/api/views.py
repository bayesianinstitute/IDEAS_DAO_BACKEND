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
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect
from ideasApi.models import (
       Otp
)
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

    
@api_view(['POST'])
def registration_view(request):
    try:
        if request.method == 'POST':
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user_data = serializer.validated_data
                user = User.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    email=user_data['email']
                )

                confirmation_subject = 'Welcome to IdeasApp! Please confirm your registration.'
                confirmation_message = f'Hi {user.username},\n\nThank you for registering at IdeasApp. \nIf you did not request this registration, please ignore this email.\n\nBest regards,\nThe IdeasApp Team'
                
                try:
                    send_mail(confirmation_subject, confirmation_message, 'noreply@yourapp.com', [user.email])
                    response_data = {
                        'status': 'success',
                        'message': 'Registration Successful! A confirmation email has been sent.',
                        'data': {
                            'username': user.username,
                            'email': user.email,
                        },
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                    response_status = status.HTTP_201_CREATED

                    user_logger = logging.getLogger('user_app.views')
                    client_ip = getattr(request, 'client_ip', '')
                    is_request_from_proxy = getattr(request, 'is_request_from_proxy', False)
                    user_logger.info(f"User registered: username={user.username}, useremail={user.email}, client_ip={client_ip}, proxy={is_request_from_proxy}")
                except Exception as email_error:
                    response_data = {
                        'status': 'failure',
                        'message': 'Registration Successful, but confirmation email could not be sent.',
                        'data': {
                            'username': user.username,
                            'email': user.email,
                        },
                        'email_error': str(email_error),
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                    response_status = status.HTTP_201_CREATED  # You can choose to use 200 or 201 here
                    
                return Response(response_data, status=response_status)
                
            else:
                response_data = {
                    'status': 'failure',
                    'errors': serializer.errors,
                    'message': 'Invalid data.',
                    'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                    'is_routable': getattr(request, 'is_routable', True),
                    'client_ip': getattr(request, 'client_ip', ''),
                    
                }
                response_status = status.HTTP_400_BAD_REQUEST
                
                return Response(response_data, status=response_status)
        else:
            response_data = {
                'status': 'failure',
                'message': 'Invalid request method.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            response_status = status.HTTP_400_BAD_REQUEST
            
            return Response(response_data, status=response_status)
            
    except ValidationError as validation_error:
        response_data = {
            'status': 'failure',
            'message': 'Invalid input data.',
            'validation_error': str(validation_error),
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
        }
        response_status = status.HTTP_400_BAD_REQUEST
        
        return Response(response_data, status=response_status)
        
    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
        }
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        return Response(response_data, status=response_status)
       

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class sent_otp(APIView):
    def post(self, request, format=None):
        try:
            serializer = OtpSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                
                user = User.objects.filter(email=email).first()
                if not user:
                    response_data = {
                        'status': 'failure',
                        'message': 'User not registered with this email',
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
                otp_instance = Otp.objects.filter(user=user).first()
                if otp_instance:
                    otp_instance.otp_value = random.randint(1000, 9999)
                    otp_instance.expiry_time = datetime.now() + timedelta(minutes=15)
                    otp_instance.save()
                else:
                    otp = random.randint(1000, 9999)
                    expiry_time = datetime.now() + timedelta(minutes=15)
                    otp_instance = Otp.objects.create(user=user, expiry_time=expiry_time, otp_value=otp)
                
                send_mail(
                    'Your OTP',
                    f'Your OTP is: {otp_instance.otp_value}',
                    'bayesdev2@gmail.com',  # Replace with your sender email
                    [email],
                    fail_silently=False,
                )
                
                response_data = {
                    'status': 'success',
                    'message': 'OTP sent successfully',
                    'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                    'is_routable': getattr(request, 'is_routable', True),
                    'client_ip': getattr(request, 'client_ip', ''),
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            response_data = {
                'status': 'failure',
                'errors': serializer.errors,
                'message': 'Invalid data.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            response_data = {
                'status': 'failure',
                'message': str(e) if str(e) else 'An error occurred.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    
class ResetPassword(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        otp_value = request.data.get("otp_value")
        data = {}
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response_data = {
                'status': 'failure',
                'message': 'User not found',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            otp_obj = Otp.objects.get(user=user)
        except Otp.DoesNotExist:
            response_data = {
                'status': 'failure',
                'message': 'OTP not generated for this user',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if otp_obj.expiry_time <= timezone.now():
            # OTP has expired
            response_data = {
                'status': 'failure',
                'message': 'OTP has expired',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.otp_value == otp_value:
            # OTP is valid
            user.password = make_password(new_password)  # Change the user's password
            user.save()  # Save the changes
            
            response_data = {
                'status': 'success',
                'message': 'Password reset successful',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Invalid OTP
            response_data = {
                'status': 'failure',
                'message': 'Invalid OTP',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
