from channels.routing import route, route_class
from .consumers import msg_consumer, AnagramsConsumer
from otree.channels.routing import channel_routing

channel_routing += [
    route_class(AnagramsConsumer, path=r"^/anagrams/(?P<channel>[a-zA-Z0-9_-]+)/$"),
    route('anagrams.word_message', msg_consumer)
]
