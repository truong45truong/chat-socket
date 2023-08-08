from django.db import models
from chat_user.user.models import User
from django.contrib.postgres.fields import ArrayField
from chat_base.core.models.base import DateTimeModel
from chat_base.core.constants.db_table import DBTable
from chat_base.core.constants.verbose_name_plural import VerboseNamePlural
from chat_base.core.constants.app_label import ModelAppLabel
from chat_base.core.constants.related_name import RelatedName
from chat_base.core.constants.db_fields import DBGroupChatFields , DBMemberFields
from chat_base.core.constants.db_fields import DBConversationFields , DBChatFields
from chat_base.core.constants.db_fields import DBNotificationFields
# Create your models here.  
import uuid 
import datetime
class GroupChat(DateTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table = DBTable.GROUPCHAT.value
        app_label = ModelAppLabel.GROUPCHAT.value
        verbose_name_plural = VerboseNamePlural.GROUPCHAT.value
        indexes = [
            models.Index(fields=[
                DBGroupChatFields.ID.value
            ])
        ]

class Member(DateTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_id = models.ForeignKey(GroupChat, related_name=RelatedName.MEMBER_GROUP, on_delete=models.CASCADE)
    is_manager = models.BooleanField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name=RelatedName.USER_MEMBERS)

    def __str__(self):
        return self.group_id
    
    class Meta:
        db_table = DBTable.MEMBER.value
        app_label = ModelAppLabel.MEMBER.value
        verbose_name_plural = VerboseNamePlural.MEMBER.value
        indexes = [
            models.Index(fields=[
                DBMemberFields.ID.value
            ])
        ] 
class Conversation(DateTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_from =  models.ForeignKey( 
        User, on_delete=models.SET_NULL, null=True,blank=True,
        related_name=RelatedName.USER_FROM_CONVERSATIONS
    )
    user_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,blank=True,
        related_name=RelatedName.USER_TO_CONVERSATIONS
    )
    group_id = models.ForeignKey(
        GroupChat, on_delete=models.SET_NULL, null=True,blank=True,
        related_name=RelatedName.CONVERSATION_GROUP
    )
    content_last = models.TextField( null = True, blank = True)
    created_at = models.DateTimeField( null = True, blank = True , default = datetime.datetime.now)
    list_user_seen = ArrayField(models.TextField())
    list_message_sent = ArrayField(models.TextField())
    user_chat = models.CharField(max_length=255)
    class Meta:
        db_table = DBTable.CONVERSATION.value
        app_label = ModelAppLabel.CONVERSATION.value
        verbose_name_plural = VerboseNamePlural.CONVERSATION.value
        indexes = [
            models.Index(fields=[
                DBConversationFields.ID.value
            ])
        ]

class Chat(DateTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id =  models.ForeignKey(
        Conversation, on_delete=models.CASCADE, null=False,blank=True,
        related_name=RelatedName.CHAT_CONVERSATION
    )
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,blank=True,
        related_name=RelatedName.CHATS_USER
    )
    content = models.TextField( null = True, blank = True)
    created_at = models.DateTimeField( null = True, blank = True , default = datetime.datetime.now)

    class Meta:
        db_table = DBTable.CHAT.value
        app_label = ModelAppLabel.CHAT.value
        verbose_name_plural = VerboseNamePlural.CHAT.value
        indexes = [
            models.Index(fields=[
                DBChatFields.ID.value
            ])
        ]

class Notification(DateTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,blank=True,
        related_name= RelatedName.NOTIFICATION_USER
    )
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.SET_NULL, null=True,blank=True,
        related_name= RelatedName.NOTIFICATION_CONVERSATION
    )
    email_user_chat = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    is_seem = models.BooleanField()
    created_at = models.DateTimeField( null = False, blank = True , default = datetime.datetime.now)

    class Meta:
        db_table = DBTable.NOTIFICATION.value
        app_label = ModelAppLabel.NOTIFICATION.value
        verbose_name_plural = VerboseNamePlural.NOTIFICATION.value
        indexes = [
            models.Index(fields=[
                DBNotificationFields.ID.value
            ])
        ]
