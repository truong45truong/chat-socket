from rest_framework import serializers
from user.models import User, Membership

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