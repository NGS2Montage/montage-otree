import arrow
import json
import logging
logger = logging.getLogger(__name__)

from channels import Group
from channels.auth import channel_session_user

from otree.models.participant import Participant
# from .models import ChatMessage

'''
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

'''

group_name = "waitPageCount"

def connect_waitPage_count(message,params):
    
    participant_code = params.split(',')[0]
    participant = Participant.objects.filter(code=participant_code).first()
    all_participants = participant.session.participant_set.all()

    n_participants =len(all_participants)
    present_participants = [p.is_on_wait_page for p in all_participants]
    n_remaining = n_participants - sum(present_participants)

    group = Group(group_name)
    group.add(message.reply_channel)

    group.send(
        {'text': json.dumps(
            {'N': n_participants, 'remaining': n_remaining}
        )}
    )

def disconnect_waitPage_count(message):

    group = Group(group_name)
    group.discard(message.reply_channel)
