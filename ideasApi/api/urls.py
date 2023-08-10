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
    path('news/<str:technology_name>/', NewsListView.as_view(), name='news-by-technology'),
    
    path('investments/', InvestmentListView.as_view(), name='investment-list'),
    path('investments/<str:technology_name>/', InvestmentListView.as_view(), name='investment-by-technology'),

    path('events/', EventsListView.as_view(), name='events-list'),
    path('events/<str:technology_name>/', EventsListView.as_view(), name='events-by-technology'),
    # other URL patterns
]


