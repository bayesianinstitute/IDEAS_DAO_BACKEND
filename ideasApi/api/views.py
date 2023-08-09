from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ideasApi.api.models import (
    News,
    Events,
    Investment,
)
from ideasApi.api.serializers import (
    NewsSerializer,
    EventsSerializer,
    InvestmentSerializer
)


class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-timing')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    
class InvestmentListView(generics.ListAPIView):
    queryset = Investment.objects.all().order_by('-timing')
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

class EventsListView(generics.ListAPIView):
    queryset = Events.objects.all().order_by('-timing')
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]




