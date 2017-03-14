import logging
logger = logging.getLogger(__name__)

from channels.generic.websockets import JsonWebsocketConsumer, WebsocketDemultiplexer

from core.bindings import ChatMessageBinding, GroupBinding, UserBinding
from .bindings import LetterTransactionBinding, TeamWordBinding, UserLetterBinding


class Demultiplexer(WebsocketDemultiplexer):
    http_user = True

    # Wire your JSON consumers here: {stream_name : consumer}
    consumers = {
        "chats": ChatMessageBinding.consumer,
        "groups": GroupBinding.consumer,
        "lettertransactions": LetterTransactionBinding.consumer,
        "teamwords": TeamWordBinding.consumer,
        "userletters": UserLetterBinding.consumer,
        "users": UserBinding.consumer,
    }

    def connection_groups(self):
        
        team_group = str(self.message.user.group.team)
        groups = [self.message.user.username + "solo", "universal-chat", team_group]
        chat_groups = [str(g) for g in self.message.user.profile.groups.all()]
        groups.extend(chat_groups)

        logger.debug("connection_groups for {}: {}".format(self.message.user, groups))
        
        return groups
