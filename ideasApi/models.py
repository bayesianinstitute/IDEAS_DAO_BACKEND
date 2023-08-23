from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import random
from ckeditor.fields import RichTextField 
from rest_framework.exceptions import ValidationError


class Technology(models.Model):
    technology_id =models.CharField(max_length=50,unique=True)
    technology_name= models.CharField(max_length=200)

    def __str__(self):
        return str(self.technology_name)
    class Meta:
        verbose_name_plural="Technology"        
        
class News(models.Model):
    def nameFile(instance, filename):
        return "/".join(["images", str(instance.news_id), filename])

    news_id =models.CharField(max_length=50,unique=True)
    title= models.CharField(max_length=200)
    brief= models.CharField(max_length=200)
    description = RichTextField()
    timestamp = models.DateTimeField(auto_now=True)
    news_image = models.FileField(null=True, blank=True)
    technologies = models.ForeignKey(
        Technology, on_delete=models.CASCADE, related_name="technologies_news"
    )
        
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="News"
        
class Investment(models.Model):
    def nameFile(instance, filename):
        return "/".join(["images", str(instance.investment_id), filename])
    investment_id =models.CharField(max_length=50,unique=True)
    title= models.CharField(max_length=200)
    description = RichTextField()
    timestamp = models.DateTimeField(auto_now=True)
    Investment_image = models.FileField(null=True, blank=True)
    technologies = models.ForeignKey(
        Technology, on_delete=models.CASCADE, related_name="technologies_investment"
    )
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Investment"
        
        
class Events(models.Model):
    def nameFile(instance, filename):
        return "/".join(["images", str(instance.event_id), filename])
    event_id =models.CharField(max_length=50,unique=True)
    title= models.CharField(max_length=200)
    description = RichTextField()
    timestamp = models.DateTimeField(auto_now=True)
    meet_time = models.DateTimeField()
    meet_link = models.URLField(max_length=200)
    event_image = models.FileField(null=True, blank=True)
    technologies = models.ForeignKey(
        Technology, on_delete=models.CASCADE, related_name="technologies_events"
    )
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Events"
        
class Proposal(models.Model):
    proposal_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)
    title= models.CharField(max_length=200)
    description = RichTextField()
    PROPOSAL_TYPE_CHOICES = (
        ('active', 'Active'),
        ('reject', 'Reject'),
        ('closed', 'Closed'),
    )
    status = models.CharField(max_length=10, choices=PROPOSAL_TYPE_CHOICES, default='active')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposaluser')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Proposal"

class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    expiry_time = models.DateTimeField()
    otp_value = models.IntegerField()

    def __str__(self):
        return str(self.otp_value)

    class Meta:
        verbose_name_plural = "Otp"


class About(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()

    def __str__(self):
        return self.title

class Device(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    device_model = models.CharField(max_length=100)
    os_version = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    proxy_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.device_id