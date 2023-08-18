from rest_framework import serializers
from django.contrib.auth.models import User
from ideasApi.models import (
        News,
        Events,
        Investment,
        Proposal
)
class NewsSerializer(serializers.ModelSerializer):
    # Your existing serializer fields go here
    class Meta:
        model = News
        fields = '__all__'
        
class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['news_image']

        
class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'
        
class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'
        
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']