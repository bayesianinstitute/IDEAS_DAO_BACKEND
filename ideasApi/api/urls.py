from django.urls import path, include
from rest_framework import routers
from ideasApi.api.views import (
    NewsListView,
    InvestmentListView,
    EventsListView,
    latest_news_images,
    get_single_news,
    get_single_investment,
    get_single_events,
    upcoming_events,
    get_about,
    create_proposal,
    ProposalList,
    ProposalByStatusList,
    UserEmailList,
    device_list,
    TechnologyList
    
)
router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    # News
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<str:technology_name>/', NewsListView.as_view(), name='news-by-technology'),
    path('latest-news-images/', latest_news_images, name='latest-news-images'),
    path('getnews/<str:news_id>/', get_single_news, name='get-single-news'),
    
    # Investment
    path('investments/', InvestmentListView.as_view(), name='investment-list'),
    path('investments/<str:technology_name>/', InvestmentListView.as_view(), name='investment-by-technology'),
    path('getinvestments/<str:investment_id>/', get_single_investment, name='get-single-investment'),

    # Events
    path('events/', EventsListView.as_view(), name='events-list'),
    path('events/<str:technology_name>/', EventsListView.as_view(), name='events-by-technology'),
    path('getevents/<str:event_id>/', get_single_events, name='get_single_events'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    
    # About
    path('about/', get_about, name='get_about'),

    #PROPOSAL
    path('create-proposal/', create_proposal, name='create-proposal'),
    path('proposals/', ProposalList.as_view(), name='proposal-list'),
    path('proposal_by_status/<str:status>/', ProposalByStatusList.as_view(), name='proposal-by-status-list'),
    path('users/emails/', UserEmailList.as_view(), name='user-email-list'),
    
    # other URL patterns
    path('devices/', device_list, name='device-list'),

    path('technologies/', TechnologyList, name='technology-list'),
]


