from django.db import models
from user.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.  
import uuid 
import datetime
class GroupChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_id = models.ForeignKey(GroupChat, related_name='member_group', on_delete=models.CASCADE)
    is_manager = models.BooleanField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='member')

    def __str__(self):
        return self.group_id
    
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_from =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='chat_user_from')
    user_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='chat_user_to')
    group_id = models.ForeignKey(GroupChat, on_delete=models.SET_NULL, null=True,blank=True,related_name='conversation_group')
    content_last = models.TextField( null = True, blank = True)
    created_at = models.DateTimeField( null = True, blank = True , default = datetime.datetime.now)
    list_user_seen = ArrayField(models.TextField())
    list_message_sent = ArrayField(models.TextField())

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id =  models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False,blank=True,related_name='chat_conversation')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='chat_user_id')
    content = models.TextField( null = True, blank = True)
    created_at = models.DateTimeField( null = True, blank = True , default = datetime.datetime.now)

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='notification_user')
    conversation_id = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True,blank=True,related_name='notification_conversation')
    email_user_chat = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    is_seem = models.BooleanField()
    created_at = models.DateTimeField( null = False, blank = True , default = datetime.datetime.now)