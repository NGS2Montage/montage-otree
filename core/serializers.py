from django.contrib.auth.models import User

from rest_framework import serializers

from .models import ChatMessage, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')
        read_only_fields = ('pk', 'username')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('user', 'profile_set')


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('user', 'message', 'room', 'created')
        extra_kwargs = {
            'room': {'write_only': True}
        }
