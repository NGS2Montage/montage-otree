import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User
from django.db.models import Q

from channels_api.bindings import ResourceBinding

from .models import ChatMessage, Group
from .serializers import ChatMessageSerializer, GroupSerializer, UserSerializer


class UserBinding(ResourceBinding):

    model = User
    stream = "users"
    serializer_class = UserSerializer

    def get_queryset(self):
        queries = Q(username=self.user.username)
        for profile in self.message.user.group.profile_set.all():
            queries |= Q(username=profile.user.username)

        return User.objects.filter(queries)

    @classmethod
    def group_names(self, instance, action):
        return [instance.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("G has_permission {} {} {}".format(user, action, pk))

        if action in ['create', 'update', 'delete']:
            return False

        # allow list, retrieve, subscribe
        return True


class GroupBinding(ResourceBinding):

    model = Group
    stream = "groups"
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(user=self.user)

    @classmethod
    def group_names(self, instance, action):
        return [instance.user.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("G has_permission {} {} {}".format(user, action, pk))

        if action in ['create', 'update', 'delete']:
            return False

        # allow list, retrieve, subscribe
        return True


class ChatMessageBinding(ResourceBinding):

    model = ChatMessage
    stream = "chats"
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.user)

    @classmethod
    def group_names(self, instance, action):
        groups = [instance.room]
        logger.debug("chatmessage group_names {} {}".format(instance, groups))

        return groups

    def create(self, data, **kwargs):
        # Sneak room into the client's create chat message
        data['room'] = str(self.user.group)
        return super(ChatMessageBinding, self).create(data, **kwargs)

    def has_permission(self, user, action, pk):
        logger.debug("CM has_permission {} {} {}".format(user, action, pk))

        if action in ['update', 'delete']:
            return False

        # allow create, list, retrieve, subscribe
        return True
