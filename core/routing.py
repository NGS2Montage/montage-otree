
from channels.routing import route
from otree.channels.routing import channel_routing
from anagrams.routing import anagrams_routing
from ultimatum.routing import ultimatum_routing
from .consumers import connect_waitPage_count, disconnect_waitPage_count
from clicktracking.routing import click_routing

channel_routing += anagrams_routing + ultimatum_routing + click_routing
channel_routing += [
    route(
        'websocket.connect', connect_waitPage_count,
        path=r'^/playerCount/(?P<params>[\w,]+)/$'),
    route(
        'websocket.disconnect', disconnect_waitPage_count,
        path=r'^/playerCount'),
]
