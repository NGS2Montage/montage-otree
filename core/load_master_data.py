import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django
django.setup()

from core.models import GameStates, Game


def load_game_states():
    GAME_STATES = [{'state_code': 'pre', 'state_name': 'Initial State the User is in', 'order': 1,
                    'allowed_user_states': [], 'url_name': 'additional-user-info'},

                   {'state_code': 'initial_survey1', 'state_name': 'Survey before game begins', 'order': 2,
                    'allowed_user_states': ['pre'], 'url_name': 'initial-survey'},

                   {'state_code': 'waiting_room1', 'state_name': 'Waiting Room 1', 'order': 3,
                    'allowed_user_states': ['pre', 'initial_survey1'], 'url_name': 'anagrams-waiting'},

                   {'state_code': 'anagrams', 'state_name': 'Anagrams Game', 'order': 4,
                    'allowed_user_states': [], 'url_name': 'anagrams-game'},

                   {'state_code': 'post_anagrams_survey', 'state_name': 'Survey After Anagrams Game', 'order': 5,
                    'allowed_user_states': [], 'url_name': 'anagrams-survey'},

                   {'state_code': 'waiting_room2', 'state_name': 'Waiting Room 2', 'order': 6,
                    'allowed_user_states': ['post_anagrams_survey'], 'url_name': 'public-goods-waiting'},

                   {'state_code': 'public_goods', 'state_name': 'Public Goods Game', 'order': 7,
                    'allowed_user_states': [], 'url_name': 'public-goods-game'},

                   {'state_code': 'post_public_goods_survey', 'state_name': 'Survey after Public Goods Game', 'order': 8,
                    'allowed_user_states': [], 'url_name': 'public-goods-survey'},

                   {'state_code': 'waiting_room3', 'state_name': 'Waiting Room 3', 'order': 9,
                    'allowed_user_states': ['post_public_goods_survey'], 'url_name': 'group-ultimatums-survey'},

                   {'state_code': 'group_ultimatums_game1', 'state_name': 'Group Ultimatums Game 1', 'order': 10,
                    'allowed_user_states': [], 'url_name': 'group-ultimatums-game-1'},

                   {'state_code': 'group_ultimatums_game2', 'state_name': 'Group Ultimatums Game 2', 'order': 11,
                    'allowed_user_states': [], 'url_name': 'group-ultimatums-game-2'},

                   {'state_code': 'group_ultimatums_game3', 'state_name': 'Group Ultimatums Game 3', 'order': 12,
                    'allowed_user_states': [], 'url_name': 'group-ultimatums-game-3'},

                   {'state_code': 'group_ultimatums_survey', 'state_name': 'Group Ultimatums Survey', 'order': 13,
                    'allowed_user_states': [], 'url_name': 'group-ultimatums-survey'}
                   ]

    print("\n" + "=" * 80 + "\n\tLOADING GAME TYPES\n" + "-" * 80)
    for state in GAME_STATES:
        stateObj, created = GameStates.objects.get_or_create(state_code=state['state_code'],
                                                             state_name=state['state_name'], order=state['order'],
                                                             url_name=state['url_name'])
        print(stateObj, created)
        for code in state['allowed_user_states']:
            allowed_state = GameStates.objects.get(state_code=code)
            print(allowed_state)
            stateObj.allowed_user_states.add(allowed_state)
            stateObj.save()
        print("\n" + "-" * 40 + "\n")


def create_game():
  Game.objects.get_or_create(game_code="initial", state=GameStates.objects.get(state_code="pre"))


if __name__ == "__main__":
    load_game_states()
    create_game()
