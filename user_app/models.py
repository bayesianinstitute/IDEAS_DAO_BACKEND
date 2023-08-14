from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    name = models.CharField(max_length=200, editable=False)  # Set editable to False
    Django_user= models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    is_valid = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural="Profile"
