from channels.routing import route, route_class
from .consumers import VoteConsumer, vote_consumer

ultimatum_routing = [
    route_class(VoteConsumer, path=r"^/votes/(?P<channel>[a-zA-Z0-9_-]+)/$"),
    route('ultimatum.vote_message', vote_consumer),
]
