from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
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
from ideasApi.models import (
    News,
    Events,
    Investment,
    Technology,
    About,
    Proposal,
    Device
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

class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum number of items per page
    
class NewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    #permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = News.objects.all().order_by('-timestamp')

        technology_name = self.kwargs.get('technology_name')
        if technology_name:
            try:
                technology = Technology.objects.get(technology_name__iexact=technology_name)
                queryset = queryset.filter(technologies=technology)
            except Technology.DoesNotExist:
                queryset = News.objects.none()

        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data['is_request_from_proxy'] = getattr(request, 'is_request_from_proxy', False)
        response.data['is_routable'] = getattr(request, 'is_routable', True)
        response.data['client_ip'] = getattr(request, 'client_ip', '')
        return response

class InvestmentListView(generics.ListAPIView):
    serializer_class = InvestmentSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Investment.objects.all().order_by('-timestamp')

        technology_name = self.kwargs.get('technology_name')
        if technology_name:
            try:
                technology = Technology.objects.get(technology_name__iexact=technology_name)
                queryset = queryset.filter(technologies=technology)
            except Technology.DoesNotExist:
                queryset = Investment.objects.none()

        return queryset
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data['is_request_from_proxy'] = getattr(request, 'is_request_from_proxy', False)
        response.data['is_routable'] = getattr(request, 'is_routable', True)
        response.data['client_ip'] = getattr(request, 'client_ip', '')
        return response

class EventsListView(generics.ListAPIView):
    serializer_class = EventsSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Events.objects.all().order_by('-timestamp')

        technology_name = self.kwargs.get('technology_name')
        if technology_name:
            try:
                technology = Technology.objects.get(technology_name__iexact=technology_name)
                queryset = queryset.filter(technologies=technology)
            except Technology.DoesNotExist:
                queryset = Events.objects.none()

        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data['is_request_from_proxy'] = getattr(request, 'is_request_from_proxy', False)
        response.data['is_routable'] = getattr(request, 'is_routable', True)
        response.data['client_ip'] = getattr(request, 'client_ip', '')
        return response
    
    


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def latest_news_images(request):
    if request.method == 'GET':
        latest_news = News.objects.order_by('-timestamp')[:5]
        serializer = NewsImageSerializer(latest_news, many=True)

        response_data = {
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
            'latest_news_images': serializer.data
        }

        return Response(response_data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_single_news(request, news_id):
    try:
        news_item = News.objects.get(news_id=news_id)
    except News.DoesNotExist:
        return Response({"error": "News item not found"}, status=404)

    if request.method == 'GET':
        serializer = NewsSerializer(news_item)
        
        response_data = {
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
            'news_item': serializer.data
        }
        
        return Response(response_data)
    
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_single_investment(request, investment_id):
    try:
        investment_item = Investment.objects.get(investment_id=investment_id)
    except Investment.DoesNotExist:
        return Response({"error": "Investment item not found"}, status=404)

    if request.method == 'GET':
        serializer = InvestmentSerializer(investment_item)
        
        response_data = {
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
            'investment_item': serializer.data
        }
        
        return Response(response_data)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_single_events(request, event_id):
    try:
        event_item = Events.objects.get(event_id=event_id)
    except Events.DoesNotExist:
        return Response({"error": "Event item not found"}, status=404)

    if request.method == 'GET':
        serializer = EventsSerializer(event_item)
        
        response_data = {
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
            'event_item': serializer.data
        }
        
        return Response(response_data)
    
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def upcoming_events(request):
    current_time = timezone.now()
    upcoming_events = Events.objects.filter(meet_time__gte=current_time).order_by('meet_time')
    serializer = EventsSerializer(upcoming_events, many=True)
    
    response_data = {
        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
        'is_routable': getattr(request, 'is_routable', True),
        'client_ip': getattr(request, 'client_ip', ''),
        'upcoming_events': serializer.data
    }
    
    return Response(response_data)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_about(request):
    about_instance = get_object_or_404(About)
    data = {
        'title': about_instance.title,
        'content': about_instance.content,
        'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
        'is_routable': getattr(request, 'is_routable', True),
        'client_ip': getattr(request, 'client_ip', ''),
    }
    return JsonResponse(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_proposal(request):
    if request.method == 'POST':
        # Get user information from the access token
        user = request.user
        
        # Create a proposal instance with the user information
        proposal_data = {
            'proposal_id': request.data.get('proposal_id'),
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'user': user.id,
        }
        
        # Create a serializer instance with the proposal data
        serializer = ProposalSerializer(data=proposal_data)
        
        if serializer.is_valid():
            serializer.save()
            
            response_data = {
                'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
                'is_routable': getattr(request, 'is_routable', True),
                'client_ip': getattr(request, 'client_ip', ''),
                'proposal_data': serializer.data,
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProposalList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Proposal.objects.all().order_by('-timestamp')
    serializer_class = ProposalSerializer
    pagination_class = CustomPagination
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        response_data = {
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
            'proposals': response.data,
        }
        
        return Response(response_data)



class ProposalByStatusList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProposalSerializer
    pagination_class = CustomPagination 
    
    def get_queryset(self):
        status = self.kwargs['status']
        queryset = Proposal.objects.filter(status=status).order_by('-timestamp')
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        response_data = {
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
            'proposals': response.data,
        }
        return Response(response_data)
    
class UserEmailList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEmailSerializer
    queryset = User.objects.all().order_by('-date_joined')[:50]
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        response_data = {
            'is_request_from_proxy': getattr(request, 'is_request_from_proxy', False),
            'is_routable': getattr(request, 'is_routable', True),
            'client_ip': getattr(request, 'client_ip', ''),
            'users': response.data,
        }
        
        return Response(response_data)
    
@api_view(['GET', 'POST'])
def device_list(request):
    if request.method == 'POST':
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)