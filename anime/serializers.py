from rest_framework import serializers

from django.contrib.auth.models import User
from notifications.models import Notification
from users.models import Profile
from anime.models import Channel




class ProfileSerializer(serializers.ModelSerializer):
    my_absolute_url = serializers.URLField(source="get_absolute_url",read_only=True) 
    class Meta:
        model = Profile
        fields = '__all__' 
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ("password",)
class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    my_absolute_url = serializers.URLField(source="action_object.get_absolute_url",read_only=True) 
    class Meta:
        model = Notification
        fields = "__all__"
        
