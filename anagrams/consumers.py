from channels import Group, Channel
from .models import Dictionary, TeamWord
from otree.models.participant import Participant
import json
from channels.generic.websockets import JsonWebsocketConsumer


def get_chat_group(channel):
    print('words-{}'.format(channel))
    return 'words-{}'.format(channel)


def msg_consumer(message):
    content = message.content

    # For now, don't create a model because we
    # don't yet have a way to export this table.
    # currently oTree admin is not extensible.

    channel = content['channel']
    word = content['word']
    channels_group = get_chat_group(channel)

    # # list containing 1 element
    # # it seems I can't use .get() because of idmap
    participant = Participant.objects.get(code=content['participant_code'])
    anagrams_player = participant.anagrams_player.first()

    anagrams_player.group.teamword_set.create(
        channel=channel,
        word=word)

    # nickname = NicknameRegistration.objects.values_list(
    #     'nickname', flat=True).get(participant=participant_id, channel=channel)

    words_message = {
        # 'channel': channel,
        'type': 'word',
        'words': [word],
        # 'participant_id': participant_id
    }

    print("I'm going to send a success word to {}".format(channels_group))
    Group(channels_group).send({'text': json.dumps(words_message)})

    # ChatMessage.objects.create(
    #     participant_id=participant_id,
    #     channel=channel,
    #     body=content['body'],
    #     nickname=nickname
    # )




class AnagramsConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        print("this guy is connected to {}".format(kwargs['channel']))
        return [get_chat_group(kwargs['channel'])]

    def connect(self, message, **kwargs):
        print("Connecting to {}".format(kwargs['channel']))
        history = TeamWord.objects.filter(
            channel=kwargs['channel']).order_by('timestamp').only('word')

        message = {
            'type': 'word',
            'words': [w.word for w in history],
        }
        self.send(message)

    def receive(self, content, **kwargs):
        # Stick the message onto the processing queue
        word = content['word']
        if not Dictionary.objects.filter(word=word).exists():
            message = {
                'type': 'error',
                'msg': "Not a valid word: {}".format(word),
            }

            self.send(message)
            return

        Channel("anagrams.word_message").send(content)
