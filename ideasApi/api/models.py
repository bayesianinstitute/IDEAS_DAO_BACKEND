from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import random
from rest_framework.exceptions import ValidationError


class Profile(models.Model):
    name = models.CharField(max_length=200)
    Django_user= models.ForeignKey(User, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural="Profile"
        
class News(models.Model):
    timing = models.DateTimeField(auto_now=True)
    title= models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="News"
        
class Investment(models.Model):
    timing = models.DateTimeField(auto_now=True)
    title= models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Investment"
        
        
class Events(models.Model):
    timing = models.DateTimeField(auto_now=True)
    title= models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Events"
        
class Proposal(models.Model):
    timing = models.DateTimeField(auto_now=True)
    title= models.CharField(max_length=200)
    description = models.TextField()
    PROPOSAL_TYPE_CHOICES = (
        ('a', 'Active'),
        ('r', 'Reject'),
        ('c', 'Closed'),
    )
    status = models.CharField(max_length=1, choices=PROPOSAL_TYPE_CHOICES, default='u')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="Proposal"
