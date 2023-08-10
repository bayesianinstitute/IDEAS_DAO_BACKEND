from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from ideasApi.api.models import (
    News,
    Events,
    Investment,
    Technology
)
from ideasApi.api.serializers import (
    NewsSerializer,
    EventsSerializer,
    InvestmentSerializer
)

class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum number of items per page
    
    
class NewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
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

class InvestmentListView(generics.ListAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
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

class EventsListView(generics.ListAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]
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