from channels.routing import route, route_class
from .consumers import msg_consumer, transaction_consumer, approval_consumer, AnagramsConsumer, TransactionConsumer
from otree.channels.routing import channel_routing

channel_routing += [
    route_class(AnagramsConsumer, path=r"^/anagrams/(?P<channel>[a-zA-Z0-9_-]+)/$"),
    route_class(TransactionConsumer, path=r"^/transactions/(?P<channel>[a-zA-Z0-9_-]+)/$"),
    route('anagrams.word_message', msg_consumer),
    route('anagrams.transaction_message', transaction_consumer),
    route('anagrams.transaction_approval', approval_consumer)
]
