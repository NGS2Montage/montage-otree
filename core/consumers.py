import arrow
import json
import logging
logger = logging.getLogger(__name__)

from channels import Group
from channels.auth import channel_session_user

from .models import ChatMessage


@channel_session_user
def chat_consumer(message):
    # Save to model
    logger.debug(message.content)
    room = message.content['room']
    ChatMessage.objects.create(
        room=room,
        message=message.content['message'],
        user=message.user
    )
    # Broadcast to listening sockets
    reply = {
        "type": "chat",
        "message": message.content['message'],
        "user": message.user.username,
        "date": arrow.now().format("YYYY-MM-DDTHH:mm:ssZ")
    }
    Group("chat-%s" % room).send({
        "text": json.dumps(reply)
    })
