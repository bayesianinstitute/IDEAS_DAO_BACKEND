from django.shortcuts import render
from rest_framework import generics


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
    
class InvestmentListView(generics.ListAPIView):
    queryset = Investment.objects.all().order_by('-timing')
    serializer_class = InvestmentSerializer

class EventsListView(generics.ListAPIView):
    queryset = Events.objects.all().order_by('-timing')
    serializer_class = EventsSerializer




