from channels import Group, Channel
from .models import Dictionary, TeamWord, UserLetter
from otree.models.participant import Participant
import json
from channels.generic.websockets import JsonWebsocketConsumer


def get_chat_group(channel):
    print('words-{}'.format(channel))
    return 'words-{}'.format(channel)

def get_transaction_group(channel):
    print('transactions-{}'.format(channel))
    return 'transactions-{}'.format(channel)


def transaction_consumer(message):
    content = message.content

    channel = content['channel']
    letter_pk = content['requested_letter']
    channels_group = get_transaction_group(channel)

    participant = Participant.objects.get(code=content['participant_code'])
    anagrams_player = participant.anagrams_player.first()

    user_letter = UserLetter.objects.get(pk=letter_pk)

    transaction = anagrams_player.lettertransaction_set.create(
        channel=channel,
        letter=user_letter)

    transaction_message = {
        'type': 'new_transaction',
        'requested_letters': [letter_pk],
    }

    owner_group = get_transaction_group(transaction.letter.player.get_transaction_channel())
    Group(owner_group).send({'text': json.dumps(transaction_message)})


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

    words_message = {
        'type': 'word',
        'words': [word],
    }

    Group(channels_group).send({'text': json.dumps(words_message)})


class TransactionConsumer(JsonWebsocketConsumer):

    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return [get_transaction_group(kwargs['channel'])]

    def connect(self, message, **kwargs):
        # print("Connecting to {}".format(kwargs['channel']))
        # history = TeamWord.objects.filter(
        #     channel=kwargs['channel']).order_by('timestamp').only('word')

        # message = {
        #     'type': 'word',
        #     'words': [w.word for w in history],
        # }
        # self.send(message)
        pass

    def receive(self, content, **kwargs):
        letter_pk = content['requested_letter']

        if not UserLetter.objects.filter(pk=letter_pk).exists():
            message = {
                'type': 'error',
                'msg': "No such letter to request: {}".format(letter_pk),
            }

            self.send(message)
            return

        # Necessary?
        message = {
            'type': 'request_success',
            'requested_letter': letter_pk,
        }
        self.send(message)

        Channel("anagrams.transaction_message").send(content)


class AnagramsConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return [get_chat_group(kwargs['channel'])]

    def connect(self, message, **kwargs):
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
