from chat_user.chat.models import GroupChat , Conversation
from chat_user.user.models import User
from rest_framework import serializers
from chat_base.core.ultis.exceptions import CustomAPIException
from chat_base.core.constants import message_code

class GroupSerializer(serializers.ModelSerializer):
    class Meta : 
        models = GroupChat
        fields = "__all__"

class ChatGroupValidSerializer(serializers.Serializer):
    conversation_id = serializers.CharField()
    user_from = serializers.EmailField()
    content_last = serializers.CharField()
    obj_conversation = serializers.SerializerMethodField()

    def get_obj_conversation(self,attrs):
        try:
            conversation_model = Conversation
            return conversation_model.objects.get(id = attrs.get('conversation_id'))
        except conversation_model.DoesNotExist:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
class GroupValidSerializer(serializers.Serializer):
    name = serializers.CharField()
    user_from = serializers.EmailField()
    description = serializers.CharField()
    list_member = serializers.JSONField()


    def validate(self, attrs):
        list_member = attrs.get('list_member')
        for member_email in list_member:
            try:
                User.objects.get(email = member_email)
            except:
                raise CustomAPIException(detail=message_code.INVALID_INPUT) 
        return super().validate(attrs)
    
class ConversationGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    group_description = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = "__all__"
    def get_group_name(self , obj):
        return obj.group_id.name
    def get_group_description(self,obj):
        return obj.group_id.description