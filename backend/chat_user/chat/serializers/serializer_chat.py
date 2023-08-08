from chat_user.chat.models import Chat , Conversation ,GroupChat , Member , Notification
from chat_user.user.models import User
from rest_framework import serializers
from django.db.models import Q
from chat_base.core.ultis.exceptions import CustomAPIException
from chat_base.core.constants import message_code



class ConversationSerializer(serializers.ModelSerializer):
    email_user_from = serializers.SerializerMethodField()
    email_user_to = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = "__all__"

    def get_email_user_from(self, obj):
        return obj.user_from.email
    def get_email_user_to(self, obj):
        return obj.user_to.email
   
class ChatSerialzier(serializers.ModelSerializer):
    email_user_chat = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = "__all__"

    def get_email_user_chat(self, obj):
        return obj.user_id.email

class MemberSerializer(serializers.ModelSerializer):
    class Meta : 
        models = Member 
        fields = "__all__"

class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ="__all__"

class ConversationValidSerializer(serializers.Serializer):
    user_from = serializers.EmailField()
    user_to = serializers.EmailField()
    content_last = serializers.CharField()
    obj_user_to = serializers.SerializerMethodField()
    def validate(self, attrs):
        conversation = Conversation.objects.filter( 
            Q(user_from__email = attrs.get('user_from') , user_to__email = attrs.get('user_to'))
            | Q(user_from__email = attrs.get('user_to'), user_to__email = attrs.get('user_from'))
        )
        print(conversation,conversation)
        if len(conversation) > 0:
            raise CustomAPIException(detail=message_code.CONVERSATION_IS_CREATED)
        return attrs
    
    def get_obj_user_to(self,attrs):
        try:
            user_model = User
            return user_model.objects.get(email = attrs.get('user_to'))
        except user_model.DoesNotExist:
            raise CustomAPIException(detail=message_code.THIS_EMAIL_NOT_YET_REGISTER)

class ChatConversationValidSerializer(serializers.Serializer):
    conversation_id = serializers.CharField()
    user_from = serializers.EmailField()
    user_to = serializers.EmailField()
    content_last = serializers.CharField()
    obj_conversation = serializers.SerializerMethodField()
    def validate(self, attrs):
        conversation = Conversation.objects.filter(
            Q(
                user_from__email = attrs.get('user_from') , 
                id = attrs.get('conversation_id') ,
                user_to__email = attrs.get('user_to')
            )
            | Q(
                user_to__email = attrs.get('user_from') , 
                id = attrs.get('conversation_id') ,
                user_from__email = attrs.get('user_to')
            )
        )
        if len(conversation) != 1:
            raise CustomAPIException(detail=message_code.THIS_EMAIL_NOT_YET_REGISTER)
        return super().validate(attrs)
    
    def get_obj_conversation(self,attrs):
        try:
            conversation_model = Conversation
            return conversation_model.objects.get(id = attrs.get('conversation_id'))
        except conversation_model.DoesNotExist:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)


        
