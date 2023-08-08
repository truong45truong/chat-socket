from rest_framework import serializers
from chat_user.user.models import User, Membership
from chat_base.core.ultis.exceptions import CustomAPIException
from chat_base.core.constants import message_code
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name' , 'email' , 'photo']
class MemberShipSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    class Meta:
        model = Membership
        fields = ['email']
    def get_email(self, obj):
        return obj.to_user.email

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self,email):
        user_check = User.objects.filter(email = email)
        if len(user_check) > 0:
            raise CustomAPIException(detail = message_code.EMAIL_USED)
        return email
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()