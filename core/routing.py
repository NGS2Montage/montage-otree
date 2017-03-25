
from otree.channels.routing import channel_routing
from anagrams.routing import anagrams_routing
from ultimatum.routing import ultimatum_routing

channel_routing += anagrams_routing + ultimatum_routing
