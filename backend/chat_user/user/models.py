from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from chat_base.core.models.base import DateTimeModel
from chat_base.core.constants.app_label import ModelAppLabel
from chat_base.core.constants.db_table import DBTable
from chat_base.core.constants.verbose_name_plural import VerboseNamePlural
from chat_base.core.constants.db_fields import DBUserFields , DBMemberShipFields
from uuid import uuid4
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
    class Meta:
        db_table = DBTable.USER.value
        app_label = ModelAppLabel.USER.value
        verbose_name_plural = VerboseNamePlural.USER.value
        indexes = [
            models.Index(fields=[
                DBUserFields.NAME.value
            ])
        ]   

class Membership(DateTimeModel):
    from_user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.user.username} - {self.to_user.user.username}"
    
    class Meta:
        db_table = DBTable.MEMBERSHIP.value
        app_label = ModelAppLabel.MEMBERSHIP.value
        verbose_name_plural = VerboseNamePlural.MEMBERSHIP.value
        indexes = [
            models.Index(fields=[
                DBMemberShipFields.FROM_USER.value
            ])
        ]  