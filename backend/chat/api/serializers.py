from chat.models import Chat , Conversation ,GroupChat , Member , Notification
from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
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
    
class ChatSerialzier(serializers.ModelSerializer):
    email_user_chat = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = "__all__"

    def get_email_user_chat(self, obj):
        return obj.user_id.email

class GroupSerializer(serializers.ModelSerializer):
    class Meta : 
        models = GroupChat
        fields = "__all__"

class MemberSerializer(serializers.ModelSerializer):
    class Meta : 
        models = Member 
        fields = "__all__"