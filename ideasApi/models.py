from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import random
from ckeditor.fields import RichTextField 
from rest_framework.exceptions import ValidationError
import jwt
from django.conf import settings
from rest_framework.authtoken.models import Token


class Technology(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural="Technology"        
        
class News(models.Model):
    def nameFile(instance, filename):
        return "/".join(["images", str(instance.news_id), filename])

    
    title= models.CharField(max_length=200)
    brief= models.CharField(max_length=200)
    description = RichTextField()
    timestamp = models.DateTimeField(auto_now=True)
    image = models.FileField(null=True, blank=True)
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
    title= models.CharField(max_length=200)
    description = RichTextField()
    timestamp = models.DateTimeField(auto_now=True)
    image = models.FileField(null=True, blank=True)
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
    title= models.CharField(max_length=200)
    description = RichTextField()
    timestamp = models.DateTimeField(auto_now=True)
    meet_time = models.DateTimeField()
    meet_link = models.URLField(max_length=200)
    image = models.FileField(null=True, blank=True)
    technologies = models.ForeignKey(
        Technology, on_delete=models.CASCADE, related_name="technologies_events"
    )
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Events"
class Member(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Encrypted password
    join_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Proposal(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    title= models.CharField(max_length=200)
    description = RichTextField()
    PROPOSAL_TYPE_CHOICES = (
        ('active', 'Active'),
        ('reject', 'Reject'),
        ('closed', 'Closed'),
    )
    status = models.CharField(max_length=10, choices=PROPOSAL_TYPE_CHOICES, default='active')
    member = models.ForeignKey(Member, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Proposal"


class About(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()

    def __str__(self):
        return self.title

    


    
class Otp(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,null=True, blank=True)
    otp_value = models.PositiveIntegerField()
    expiry_time = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.member.username}"

    
class Device(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,null=True, blank=True)
    device_model = models.CharField(max_length=100,null=True, blank=True)
    os_version = models.CharField(max_length=50,null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    proxy_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.device_model
        
class Delegate(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,null=True, blank=True)
    wallet_address = models.CharField(max_length=100,null=True, blank=True)
    coin_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.username} - {self.wallet_address}"
    
class Test(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural="Test"   
