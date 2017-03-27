from channels import Group, Channel
from .models import Dictionary, TeamWord, UserLetter, LetterTransaction, Player
from otree.models.participant import Participant
import json
from channels.generic.websockets import JsonWebsocketConsumer


def get_chat_group(channel):
    return 'words-{}'.format(channel)

def get_transaction_group(channel):
    return 'transactions-{}'.format(channel)


def approval_consumer(message):
    content = message.content

    transaction_pk = content['transaction_pk']
    transaction = LetterTransaction.objects.get(pk=transaction_pk)
    transaction.approved = True
    transaction.save()

    approval_message = {
        'type': 'transaction_approved',
        'transaction_pk': transaction.pk
    }

    group = get_transaction_group(transaction.channel)
    Group(group).send({'text': json.dumps(approval_message)})


def transaction_consumer(message):
    content = message.content

    channel = content['channel']
    letter_pk = content['requested_letter']
    channels_group = get_transaction_group(channel)

    participant = Participant.objects.get(code=content['participant_code'])
    anagrams_player = participant.anagrams_player.first()

    user_letter = UserLetter.objects.get(pk=letter_pk)
    owner_channel = user_letter.player.get_transaction_channel()

    transaction = anagrams_player.lettertransaction_set.create(
        channel=channel,
        owner_channel=owner_channel,
        letter=user_letter)

    requester_message = {
        'type': 'request_success',
        'requested_letters': [transaction.to_dict()]
    }
    requester_group = get_transaction_group(channel)
    Group(requester_group).send({'text': json.dumps(requester_message)})

    owner_message = {
        'type': 'new_transaction',
        'requested_letters': [transaction.to_dict()]
    }
    owner_group = get_transaction_group(owner_channel)
    Group(owner_group).send({'text': json.dumps(owner_message)})


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
        history = LetterTransaction.objects.filter(
            channel=kwargs['channel']).order_by('timestamp').only('letter')

        message = {
            'type': 'request_success',
            'requested_letters': [transaction.to_dict() for transaction in history]
        }
        self.send(message)

        history = LetterTransaction.objects.filter(
            owner_channel=kwargs['channel']).order_by('timestamp').only('letter')

        message = {
            'type': 'new_transaction',
            'requested_letters': [transaction.to_dict() for transaction in history]
        }
        self.send(message)

    def receive(self, content, **kwargs):
        channel = content['channel']
        msg_type = content['type']

        if msg_type == "request_approved":
            transaction_pk = content['transaction_pk']
            transaction = LetterTransaction.objects.filter(pk=transaction_pk)

            if transaction.count() == 0:
                message = {
                    'type': 'error',
                    'msg': "No such letter transaction to approve: {}".format(transaction_pk),
                }

                self.send(message)
                return

            Channel("anagrams.transaction_approval").send(content)

        if msg_type == "letter_request":
            letter_pk = content['requested_letter']

            if not UserLetter.objects.filter(pk=letter_pk).exists():
                message = {
                    'type': 'error',
                    'msg': "No such letter to request: {}".format(letter_pk),
                }

                self.send(message)
                return

            user_letter = UserLetter.objects.get(pk=letter_pk)
            if LetterTransaction.objects.filter(letter=user_letter, channel=channel).exists():
                message = {
                    'type': 'error',
                    'msg': "Letter {} already requested from {}".format(user_letter.letter, user_letter.player.chat_nickname()),
                }

                self.send(message)
                return

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
        channel = content['channel']
        participant_code = content['participant_code']

        if not Dictionary.objects.filter(word=word).exists():
            message = {
                'type': 'error',
                'msg': "Not a valid word: {}".format(word),
            }

            self.send(message)
            return

        participant = Participant.objects.get(code=participant_code)
        player = participant.anagrams_player.first()
        available_letters = [letter.letter for letter in player.userletter_set.all()]

        transaction_channel = player.get_transaction_channel()
        my_transactions = LetterTransaction.objects.filter(channel=transaction_channel, approved=True)
        for transaction in my_transactions:
            available_letters.append(transaction.letter.letter)

        for letter in word:
            if letter.upper() not in available_letters:
                message = {
                    'type': 'error',
                    'msg': "Letter '{}' not available for {}".format(letter, word),
                }

                self.send(message)
                return

        if TeamWord.objects.filter(channel=channel, word=word).exists():
            message = {
                'type': 'error',
                'msg': "Word has already been played: {}".format(word),
            }

            self.send(message)
            return

        Channel("anagrams.word_message").send(content)
