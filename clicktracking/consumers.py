from channels import Channel
from .models import Click
from otree.models.participant import Participant
from channels.generic.websockets import JsonWebsocketConsumer


def click_message(message):
    content = message.content

    element = content['element']
    participant_code = content['participant_code']
    timestamp = content['timestamp']

    participant = Participant.objects.get(code=participant_code)
    Click.objects.create(participant=participant, element=element, timestamp=timestamp)


class ClickConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        return [kwargs['channel']]

    def connect(self, message, **kwargs):
        pass

    def receive(self, content, **kwargs):
        # Stick the message onto the processing queue so this worked can relax
        Channel("clicktracking.click").send(content)
