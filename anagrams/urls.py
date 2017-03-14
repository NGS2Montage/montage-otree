from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^survey/', views.survey, name="anagrams-survey"),
    url(r'^tutorial/', views.tutorial, name="anagrams-tutorial"),
    url(r'^waiting-room/', views.waiting_room, name="anagrams-waiting"),
    url(r'^part1/', views.game, name="anagrams-game"),
]
