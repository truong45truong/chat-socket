from chat.models import Chat , Conversation
from rest_framework import serializers


class ConversationSerializer(serializers.Serializer):
    class Meta:
        model = Conversation
        fields = "__all__"
class ChatSerialzier(serializers.Serializer):
    class Meta:
        model = Chat
        fields = "__all__"