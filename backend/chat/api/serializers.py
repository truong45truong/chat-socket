from chat.models import Chat , Conversation
from rest_framework import serializers


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