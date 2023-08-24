from rest_framework import serializers
from django.contrib.auth.models import User
from ideasApi.models import (
        News,
        Events,
        Investment,
        Proposal,
        Device
)
class NewsSerializer(serializers.ModelSerializer):
    technology_name = serializers.SerializerMethodField()

    def get_technology_name(self, news):
        return news.technologies.technology_name
    
    class Meta:
        model = News
        fields = ('news_id', 'title', 'brief', 'description', 'timestamp', 'news_image', 'technology_name')
        
class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['news_image', 'news_id']

        
class EventsSerializer(serializers.ModelSerializer):
    technology_name = serializers.SerializerMethodField()

    def get_technology_name(self, event):
        return event.technologies.technology_name
    
    class Meta:
        model = Events
        fields = ('event_id', 'title', 'description', 'timestamp', 'meet_time', 'meet_link', 'event_image', 'technology_name')
        
        
class InvestmentSerializer(serializers.ModelSerializer):
    technology_name = serializers.SerializerMethodField()

    def get_technology_name(self, investment):
        return investment.technologies.technology_name
    
    class Meta:
        model = Investment
        fields = ('investment_id', 'title', 'description', 'timestamp', 'Investment_image', 'technology_name')
        
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
        
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'