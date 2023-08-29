from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
import ipaddress
from rest_framework import viewsets
from ipware import get_client_ip
from ideasApi.authentication import MemberJWTAuthentication,CustomIsAuthenticated

from ideasApi.models import (
    News,
    Events,
    Investment,
    Technology,
    About,
    Proposal,
    Device,
    Member
)

from ideasApi.api.serializers import (
    NewsSerializer,
    EventsSerializer,
    InvestmentSerializer,
    NewsImageSerializer,
    ProposalSerializer,
    UserEmailSerializer,
    DeviceSerializer
)
import logging
from ideasApi.middleware import ProxyDetectionMiddleware
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND

class CustomPagination(PageNumberPagination):
    page_size = 2 # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum number of items per page
    
class NewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = News.objects.all().order_by('-timestamp')

        technology_name = self.kwargs.get('technology_name')
        if technology_name:
            try:
                technology = Technology.objects.get(name__iexact=technology_name)
                queryset = queryset.filter(technologies=technology)
            except Technology.DoesNotExist:
                queryset = News.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                page = self.paginate_queryset(queryset)
                serializer = self.get_serializer(page, many=True)
                response_data = {
                    "status": "success",
                    "pagination": {
                        "count": self.paginator.page.paginator.count,
                        "next": self.paginator.get_next_link(),
                        "previous": self.paginator.get_previous_link(),
                        "data": serializer.data
                    },
                    "message": "Request successful.",
                    "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                    "is_routable": getattr(request, 'is_routable', True),
                    "client_ip": getattr(request, 'client_ip', '')
                }
                response_status = status.HTTP_200_OK
            else:
                response_data = {
                    "status": "success",
                    "message": "No data available.",
                    "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                    "is_routable": getattr(request, 'is_routable', True),
                    "client_ip": getattr(request, 'client_ip', '')
                }
                response_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            response_data = {
                "status": "failure",
                "message": str(e) if str(e) else "An error occurred.",
                "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                "is_routable": getattr(request, 'is_routable', True),
                "client_ip": getattr(request, 'client_ip', '')
            }
            response_status = status.HTTP_400_BAD_REQUEST
        
        response = Response(response_data, status=response_status)
        
        return response

class InvestmentListView(generics.ListAPIView):
    serializer_class = InvestmentSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Investment.objects.all().order_by('-timestamp')

        technology_name = self.kwargs.get('technology_name')
        if technology_name:
            try:
                technology = Technology.objects.get(name__iexact=technology_name)
                queryset = queryset.filter(technologies=technology)
            except Technology.DoesNotExist:
                queryset = Investment.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                page = self.paginate_queryset(queryset)
                serializer = self.get_serializer(page, many=True)
                response_data = {
                    "status": "success",
                    "pagination": {
                        "count": self.paginator.page.paginator.count,
                        "next": self.paginator.get_next_link(),
                        "previous": self.paginator.get_previous_link(),
                        "data": serializer.data
                    },
                    "message": "Request successful.",
                    "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                    "is_routable": getattr(request, 'is_routable', True),
                    "client_ip": getattr(request, 'client_ip', '')
                }
                response_status = HTTP_200_OK
            else:
                response_data = {
                    "status": "success",
                    "message": "No data available.",
                    "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                    "is_routable": getattr(request, 'is_routable', True),
                    "client_ip": getattr(request, 'client_ip', '')
                }
                response_status = HTTP_400_BAD_REQUEST
        except Exception as e:
            response_data = {
                "status": "failure",
                "message": str(e) if str(e) else "An error occurred.",
                "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                "is_routable": getattr(request, 'is_routable', True),
                "client_ip": getattr(request, 'client_ip', '')
            }
            response_status = HTTP_400_BAD_REQUEST
        
        response = Response(response_data, status=response_status)
        
        return response

class EventsListView(generics.ListAPIView):
    serializer_class = EventsSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Events.objects.all().order_by('-timestamp')

        technology_name = self.kwargs.get('technology_name')
        if technology_name:
            try:
                technology = Technology.objects.get(name__iexact=technology_name)
                queryset = queryset.filter(technologies=technology)
            except Technology.DoesNotExist:
                queryset = Events.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                page = self.paginate_queryset(queryset)
                serializer = self.get_serializer(page, many=True)
                response_data = {
                    "status": "success",
                    "pagination": {
                        "count": self.paginator.page.paginator.count,
                        "next": self.paginator.get_next_link(),
                        "previous": self.paginator.get_previous_link(),
                        "data": serializer.data
                    },
                    "message": "Request successful.",
                    "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                    "is_routable": getattr(request, 'is_routable', True),
                    "client_ip": getattr(request, 'client_ip', '')
                }
                response_status = HTTP_200_OK
            else:
                response_data = {
                    "status": "success",
                    "message": "No data available.",
                    "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                    "is_routable": getattr(request, 'is_routable', True),
                    "client_ip": getattr(request, 'client_ip', '')
                }
                response_status = HTTP_400_BAD_REQUEST
        except Exception as e:
            response_data = {
                "status": "failure",
                "message": str(e) if str(e) else "An error occurred.",
                "is_request_from_proxy": getattr(request, 'is_request_from_proxy', False),
                "is_routable": getattr(request, 'is_routable', True),
                "client_ip": getattr(request, 'client_ip', '')
            }
            response_status = HTTP_400_BAD_REQUEST
        
        response = Response(response_data, status=response_status)
        
        return response



@api_view(['GET'])
def latest_news_images(request):
    try:
        if request.method == 'GET':
            latest_news = News.objects.order_by('-timestamp')[:5]
            
            if latest_news.exists():
                serializer = NewsImageSerializer(latest_news, many=True, context={'request': request})  # Pass the request to serializer context
                response_data = {
                    "status": "success",
                    "data": serializer.data,
                    "message": "Request successful."
                }
                response_status = HTTP_200_OK
            else:
                response_data = {
                    "status": "success",
                    "message": "No data available."
                }
                response_status = HTTP_400_BAD_REQUEST
    except Exception as e:
        response_data = {
            "status": "failure",
            "message": str(e) if str(e) else "An error occurred."
        }
        response_status = HTTP_400_BAD_REQUEST

    response = Response(response_data, status=response_status)

    response.data['is_request_from_proxy'] = getattr(request, 'is_request_from_proxy', False)
    response.data['is_routable'] = getattr(request, 'is_routable', True)
    response.data['client_ip'] = getattr(request, 'client_ip', '')

    return response


@api_view(['GET'])
def get_single_news(request, news_id):
    try:
        news_item = News.objects.get(id=news_id)
        serializer = NewsSerializer(news_item, context={'request': request})  # Pass the request to serializer context
        response_data = {
            'status': 'success',
            'data': serializer.data,  # Use the serialized data directly
            'message': 'Request successful.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_200_OK
    except News.DoesNotExist:
        response_data = {
            'status': 'success',
            'message': 'News item not found.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_404_NOT_FOUND
    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_400_BAD_REQUEST

    response = Response(response_data, status=response_status)
    return response


    
@api_view(['GET'])
def get_single_investment(request, investment_id):
    try:
        investment_item = Investment.objects.get(id=investment_id)
        serializer = InvestmentSerializer(investment_item, context={'request': request})  # Pass the request to serializer context
        response_data = {
            'status': 'success',
            'data': serializer.data,  # Use the serialized data directly
            'message': 'Request successful.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_200_OK
    except Investment.DoesNotExist:
        response_data = {
            'status': 'success',
            'message': 'Investment item not found.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_404_NOT_FOUND
    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_400_BAD_REQUEST

    response = Response(response_data, status=response_status)
    return response

    
@api_view(['GET'])
def get_single_events(request, event_id):
    try:
        event_item = Events.objects.get(id=event_id)
        serializer = EventsSerializer(event_item, context={'request': request})  # Pass the request to serializer context
        response_data = {
            'status': 'success',
            'data': serializer.data,  # Use the serialized data directly
            'message': 'Request successful.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_200_OK
    except Events.DoesNotExist:
        response_data = {
            'status': 'success',
            'message': 'Event item not found.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_404_NOT_FOUND
    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_400_BAD_REQUEST

    response = Response(response_data, status=response_status)
    return response

    
    
@api_view(['GET'])
def upcoming_events(request):
    try:
        current_time = timezone.now()
        upcoming_events = Events.objects.filter(meet_time__gte=current_time).order_by('meet_time')
        
        if upcoming_events.exists():
            serializer = EventsSerializer(upcoming_events, many=True, context={'request': request})  # Pass the request to serializer context
            response_data = {
                'status': 'success',
                'data': serializer.data,
                'message': 'Request successful.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', '')
            }
            response_status = HTTP_200_OK
        else:
            response_data = {
                'status': 'success',
                'message': 'No data available.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', '')
            }
            response_status = HTTP_200_OK

    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', '')
        }
        response_status = HTTP_400_BAD_REQUEST
    
    response = Response(response_data, status=response_status)
    return response



@api_view(['GET'])
@authentication_classes([MemberJWTAuthentication])
@permission_classes([CustomIsAuthenticated])
def get_about(request):
    try:
        about_instance = get_object_or_404(About)
        data = {
            'title': about_instance.title,
            'content': about_instance.content,
        }
        response_data = {
            'status': 'success',
            'data': data,
            'message': 'Request successful.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
        }
        response_status = HTTP_200_OK
    except About.DoesNotExist:
        response_data = {
            'status': 'success',
            'message': 'No data available.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
        }
        response_status = HTTP_404_NOT_FOUND
    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
        }
        response_status = HTTP_400_BAD_REQUEST
    
    response = Response(response_data, status=response_status)
    return response



@api_view(['POST'])
@authentication_classes([MemberJWTAuthentication])
@permission_classes([CustomIsAuthenticated])
def create_proposal(request):
    if request.method == 'POST':
        # Get user information from the access token
        user = request.user

        # Create a proposal instance with the user information
        proposal_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'member': user.id,
        }
        
        # Check if a proposal with the same title already exists
        existing_proposal = Proposal.objects.filter(title=proposal_data['title']).exists()
        if existing_proposal:
            response_data = {
                'status': 'failure',
                'message': 'A proposal with the same title already exists.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            # Create a serializer instance with the proposal data
            serializer = ProposalSerializer(data=proposal_data)
        
            if serializer.is_valid():
                serializer.save()
                
                # Get the username for the user
                user_instance = Member.objects.get(pk=user.id)
                user_name = user_instance.username
            
                response_data = {
                    'status': 'success',
                    'data': {
                        'id': serializer.data['id'],
                        'timestamp': serializer.data['timestamp'],
                        'title': serializer.data['title'],
                        'description': serializer.data['description'],
                        'status': serializer.data['status'],
                        'user': user_name,  # Use the username
                    },
                    'message': 'Proposal created successfully.',
                    'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                    'is_routable': getattr(request, 'is_routable', True),
                    'client_ip': getattr(request, 'client_ip', ''),
                }
                response_status = status.HTTP_201_CREATED
            else:
                response_data = {
                    'status': 'failure',
                    'message': 'Failed to create proposal.',
                    'errors': serializer.errors,
                    'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                    'is_routable': getattr(request, 'is_routable', True),
                    'client_ip': getattr(request, 'client_ip', ''),
                }
                response_status = status.HTTP_400_BAD_REQUEST
        
        response = Response(response_data, status=response_status)
        return response

    
    
class ProposalList(generics.ListAPIView):
    authentication_classes  = [MemberJWTAuthentication] 
    permission_classes= [CustomIsAuthenticated]
    serializer_class = ProposalSerializer
    pagination_class = CustomPagination


    def get_queryset(self):
        queryset = Proposal.objects.all().order_by('-timestamp')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            if not queryset.exists():
                response_data = {
                    'status': 'success',
                    'message': 'No data available.',
                    'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                    'is_routable': getattr(request, 'is_routable', True),
                    'client_ip': getattr(request, 'client_ip', ''),
                }
                response_status = status.HTTP_200_OK
            else:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    pagination_response = self.paginator.get_paginated_response(serializer.data).data
                    response_data = {
                        'status': 'success',
                        'pagination': {
                            'count': pagination_response['count'],
                            'next': pagination_response['next'],
                            'previous': pagination_response['previous'],
                            'data': pagination_response['results'],
                        },
                        'message': 'Request successful.',
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                else:
                    response_data = {
                        'status': 'success',
                        'message': 'No data available.',
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                response_status = status.HTTP_200_OK
        except Exception as e:
            response_data = {
                'status': 'failure',
                'message': str(e) if str(e) else 'An error occurred.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            response_status = status.HTTP_400_BAD_REQUEST

        response = Response(response_data, status=response_status)
        return response

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists():
            return self.list(request, *args, **kwargs)
        else:
            response_data = {
                'status': 'success',
                'message': 'No data available.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            response_status = status.HTTP_200_OK
            response = Response(response_data, status=response_status)
            return response




class ProposalByStatusList(generics.ListAPIView):
    authentication_classes  = [MemberJWTAuthentication] 
    permission_classes= [CustomIsAuthenticated]
    serializer_class = ProposalSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        status = self.kwargs['status']
        queryset = Proposal.objects.filter(status=status).order_by('-timestamp')
        return queryset
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            if not queryset.exists():
                response_data = {
                    'status': 'success',
                    'message': 'No data available.',
                    'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                    'is_routable': getattr(request, 'is_routable', True),
                    'client_ip': getattr(request, 'client_ip', ''),
                }
                response_status = status.HTTP_200_OK
            else:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    pagination_response = self.paginator.get_paginated_response(serializer.data).data
                    response_data = {
                        'status': 'success',
                        'pagination': {
                            'count': pagination_response['count'],
                            'next': pagination_response['next'],
                            'previous': pagination_response['previous'],
                            'data': pagination_response['results'],  # Extract the 'results' field from pagination_response
                        },
                        'message': 'Request successful.',
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                else:
                    response_data = {
                        'status': 'success',
                        'message': 'No data available.',
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                response_status = status.HTTP_200_OK
        except Exception as e:
            response_data = {
                'status': 'failure',
                'message': str(e) if str(e) else 'An error occurred.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            response_status = status.HTTP_400_BAD_REQUEST
        
        response = Response(response_data, status=response_status)
        return response

       
    
class UserEmailList(generics.ListAPIView):
    authentication_classes  = [MemberJWTAuthentication] 
    permission_classes= [CustomIsAuthenticated]
    serializer_class = UserEmailSerializer
    queryset = Member.objects.all().order_by('-join_time')[:50]
    pagination_class = CustomPagination  # You might want to include pagination as well

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            if not queryset.exists():
                response_data = {
                    'status': 'success',
                    'message': 'No users available.',
                    'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                    'is_routable': getattr(request, 'is_routable', True),
                    'client_ip': getattr(request, 'client_ip', ''),
                }
                response_status = status.HTTP_200_OK
            else:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    pagination_response = self.paginator.get_paginated_response(serializer.data).data
                    response_data = {
                        'status': 'success',
                        'pagination': {
                            'count': pagination_response['count'],
                            'next': pagination_response['next'],
                            'previous': pagination_response['previous'],
                            'data': pagination_response['results'],  # Renamed 'data' to 'users'
                        },
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                else:
                    response_data = {
                        'status': 'success',
                        'message': 'No users available.',
                        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                        'is_routable': getattr(request, 'is_routable', True),
                        'client_ip': getattr(request, 'client_ip', ''),
                    }
                response_status = status.HTTP_200_OK
        except Exception as e:
            response_data = {
                'status': 'failure',
                'message': str(e) if str(e) else 'An error occurred.',
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
            }
            response_status = status.HTTP_400_BAD_REQUEST
        
        response = Response(response_data, status=response_status)
        return response

    
@api_view(['GET', 'PUT'])
@authentication_classes([MemberJWTAuthentication])
@permission_classes([CustomIsAuthenticated])
def device_list(request):
    try:
        member = request.user  # Using the authenticated member directly
        try:
            device = Device.objects.get(member=member)
        except Device.DoesNotExist:
            device = None
            
        if request.method == 'PUT':
            serializer = DeviceSerializer(device, data=request.data)
            if serializer.is_valid():
                serializer.save(member=member)  # Associate the member with the device
                response_data = {
                    'status': 'success',
                    'data': [serializer.data],  # Wrap the data in a list
                    'message': 'Device information updated successfully.',
                }
                response_status = status.HTTP_200_OK
            else:
                response_data = {
                    'status': 'failure',
                    'message': 'Invalid data.',
                }
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            if device:
                response_data = {
                    'status': 'success',
                    'data': [DeviceSerializer(device).data],  # Wrap the data in a list
                    'message': 'Device information retrieved successfully.',
                }
            else:
                response_data = {
                    'status': 'failure',
                    'message': 'Device not found.',
                }
            response_status = status.HTTP_200_OK
        
    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
        }
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    response_data.update({
        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
        'is_routable': getattr(request, 'is_routable', True),
        'client_ip': getattr(request, 'client_ip', ''),
    })
    
    response = Response(response_data, status=response_status)
    return response

@api_view(['GET'])
def TechnologyList(request, format=None):
    try:
        # Get all technologies from the database
        technologies = Technology.objects.all()

        # Serialize the technologies
        serialized_technologies = [
            {
                "id": tech.id,
                "name": tech.name
            }
            for tech in technologies
        ]

        response_data = {
            'status': 'success',
            'data': serialized_technologies,
            'message': 'Technologies retrieved successfully.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
        }
        response_status = status.HTTP_200_OK

    except Exception as e:
        response_data = {
            'status': 'failure',
            'message': str(e) if str(e) else 'An error occurred.',
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
        }
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    response = Response(response_data, status=response_status)
    return response
