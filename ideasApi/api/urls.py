from django.urls import path, include
from rest_framework import routers
from ideasApi.api.views import (
    NewsListView,
    InvestmentListView,
    EventsListView,
    
    
)
router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('investment/', InvestmentListView.as_view(), name='investment-list'),
    path('events/', EventsListView.as_view(), name='events-list'),
]


