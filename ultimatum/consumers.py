from channels import Group, Channel
# from .models import Vote
from otree.models.participant import Participant
import json
from channels.generic.websockets import JsonWebsocketConsumer

def get_vote_group(channel):
    print('voting-{}'.format(channel))
    return 'voting-{}'.format(channel)


def vote_consumer(message):
    content = message.content
    neighbor_id = content['neighbor_id']

    ultimatum_player = Participant.objects.get(code=content['participant_code']).ultimatum_player.first()
    neighbor = ultimatum_player.neighbors.get(id=neighbor_id)

    neighbor_channel = neighbor.get_vote_channel()
    neighbor_group = get_vote_group(neighbor_channel)

    vote_message = {
        'type': 'vote',
        'votes': ["{} thinks you should {} your suggestion".format(ultimatum_player.nickname(), 'increase' if content['voteUp'] else 'decrease')],
    }

    print("Sending to {}: {}".format(neighbor_group, vote_message))
    Group(neighbor_group).send({'text': json.dumps(vote_message)})


class VoteConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return [get_vote_group(kwargs['channel'])]

    def connect(self, message, **kwargs):
        # history = TeamWord.objects.filter(
        #     channel=kwargs['channel']).order_by('timestamp').only('word')

        # message = {
        #     'type': 'word',
        #     'words': [w.word for w in history],
        # }
        # self.send(message)
        pass

    def receive(self, content, **kwargs):
        print("Received something on vote socket {}".format(content))

        neighbor_id = content['neighbor_id']
        participant = Participant.objects.get(code=content['participant_code'])
        neighbors = participant.ultimatum_player.first().neighbors

        if not neighbors.filter(id=neighbor_id).exists():
            message = {
                'type': 'error',
                'msg': "No such neighbor with ID: {}".format(neighbor_id),
            }

            self.send(message)
            return

        Channel("ultimatum.vote_message").send(content)
