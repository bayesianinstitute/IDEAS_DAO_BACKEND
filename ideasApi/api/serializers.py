from rest_framework import serializers
from django.contrib.auth.models import User
from ideasApi.models import (
        News,
        Events,
        Investment,
        Proposal,
        Device,
        Member
)
class NewsSerializer(serializers.ModelSerializer):
    technology_name = serializers.SerializerMethodField()

    def get_technology_name(self, news):
        return news.technologies.name
    
    class Meta:
        model = News
        fields = ('id', 'title', 'brief', 'description', 'timestamp', 'image', 'technology_name')
        
class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'image']

        
class EventsSerializer(serializers.ModelSerializer):
    technology_name = serializers.SerializerMethodField()

    def get_technology_name(self, event):
        return event.technologies.name
    
    class Meta:
        model = Events
        fields = ('id', 'title', 'description', 'timestamp', 'meet_time', 'meet_link', 'image', 'technology_name')
        
        
class InvestmentSerializer(serializers.ModelSerializer):
    technology_name = serializers.SerializerMethodField()

    def get_technology_name(self, investment):
        return investment.technologies.name
    
    class Meta:
        model = Investment
        fields = ('id', 'title', 'description', 'timestamp', 'image', 'technology_name')
        
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['email']
        
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'