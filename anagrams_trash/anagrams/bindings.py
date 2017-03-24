import json
import logging
logger = logging.getLogger(__name__)

from django.db.models import Q

from channels_api.bindings import ResourceBinding

from .models import LetterTransaction, UserLetter, TeamWord, Dictionary
from .serializers import LetterTransactionSerializer, UserLetterSerializer, TeamWordSerializer


class TeamWordBinding(ResourceBinding):

    model = TeamWord
    stream = "teamwords"
    serializer_class = TeamWordSerializer

    def get_queryset(self):
        return TeamWord.objects.filter(user__group__team=self.user.group.team)

    @classmethod
    def group_names(self, instance, action):
        return [str(instance.user.group.team)]

    def has_permission(self, user, action, pk):
        logger.debug("TW has_permission {} {} {}".format(user, action, pk))

        if action in ['update', 'delete']:
            return False

        if action == 'create':
            payload = json.loads(self.message.content['text'])
            if 'data' not in payload or 'word' not in payload['data']:
                logger.debug("Possibly malicious malformed TeamWord from {}".format(self.user.username))
                return False

            word = payload['data']['word']
            word_letters = set(word.lower())
            if len(word_letters) == 0:
                return False

            user = self.user
            user_letters = set()
            for letter in UserLetter.objects.filter(user=user):
                user_letters.add(letter.letter.lower())
            for letter in LetterTransaction.objects.filter(borrower=user, approved=True):
                user_letters.add(letter.letter.lower())

            if not word_letters.issubset(user_letters):
                return False

            team_words = set()
            for tword in self.get_queryset():
                team_words.add(tword.word)

            if word in team_words:
                return False

            try:
                wordObj = Dictionary.objects.get(word=word)
            except Exception as e:
                return False

            return True

        # allow list, retrieve, subscribe
        return True

     
class UserLetterBinding(ResourceBinding):

    model = UserLetter
    stream = "userletters"
    serializer_class = UserLetterSerializer

    def get_queryset(self):
        queries = Q(user=self.user)
        for profile in self.message.user.group.profile_set.all():
            queries |= Q(user=profile.user)

        return UserLetter.objects.filter(queries)

    @classmethod
    def group_names(self, instance, action):
        logger.debug(str(instance))
        return [instance.user.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("UL has_permission {} {} {}".format(user, action, pk))

        if action in ['create', 'update', 'delete']:
            return False

        # allow list, retrieve, subscribe
        return True


class LetterTransactionBinding(ResourceBinding):

    model = LetterTransaction
    stream = "lettertransactions"
    serializer_class = LetterTransactionSerializer

    def get_queryset(self):
        return LetterTransaction.objects.filter(Q(borrower=self.user) | Q(letter__user=self.user))

    @classmethod
    def group_names(self, instance, action):
        # Send this to only the borrower and lender
        return [instance.borrower.username + "solo", instance.letter.user.username + "solo"]

    def has_permission(self, user, action, pk):
        logger.debug("TR has_permission {} {} {}".format(user, action, self.message.content['text']))

        if action == "delete":
            return False

        if action == "create" or action == "update":
            payload = json.loads(self.message.content['text'])
            if 'data' not in payload or 'letter' not in payload['data']:
                logger.debug("Possibly malicious malformed LetterTransaction from {}".format(self.user.username))
                return False

            ul = UserLetter.objects.get(pk=payload['data']['letter'])

            # If this UserLetter is not owned by a friend, permission denied
            if ul.user.profile not in self.user.group.profile_set.all():
                logger.debug("Malicious LetterTransaction creation suspected by {}".format(self.user.username))
                return False

        # allow list, retrieve, subscribe, and legitimate create
        return True
