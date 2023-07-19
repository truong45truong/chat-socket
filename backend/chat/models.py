from django.db import models
from user.models import User
# Create your models here.  
import uuid 
import datetime
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_from =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='chat_user_from')
    user_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='chat_user_to')
    content_last = models.TextField( null = True, blank = True)
    created_at = models.DateTimeField( null = True, blank = True , default = datetime.datetime.now)
class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id =  models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False,blank=True,related_name='chat_conversation')
    content = models.TextField( null = True, blank = True)
    created_at = models.DateTimeField( null = True, blank = True , default = datetime.datetime.now)
