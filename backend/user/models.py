from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.conf import settings
import shutil
import os
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo    = models.ImageField(upload_to =  'media/photos/user', height_field = None, width_field = None, max_length = None)
    name     = models.CharField( max_length=255 )
    password = models.CharField( max_length = 255)
    email    = models.EmailField(unique = True , max_length = 255)
    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return  self.email

    def __unicode__(self):
        return self

class Membership(models.Model):
    from_user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.user.username} - {self.to_user.user.username}"