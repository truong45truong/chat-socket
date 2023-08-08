from chat_user.chat.models import Notification
from rest_framework import serializers
from chat_base.core.ultis.exceptions import CustomAPIException
from chat_base.core.constants import message_code
from chat_user.user.models import User
from chat_user.chat.models import Conversation

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class NotificationValidSerializer(serializers.Serializer):
    content = serializers.CharField()
    email_user_chat = serializers.EmailField()
    conversation_id = serializers.JSONField()
    type = serializers.CharField()

    def validate_email_user_chat(self, email_user_chat) -> str:
        try:
            User.objects.get(email = email_user_chat)
        except :
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        return email_user_chat
    
    def validate_conversation_id(self, conversation_id) -> object:
        try:
            conversaion = Conversation.objects.get(id = conversation_id)
        except :
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        return conversaion