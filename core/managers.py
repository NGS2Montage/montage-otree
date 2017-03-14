from django.db import models


class GameManager(models.Manager):
    def get_current_game(self):
        all_games = super(GameManager, self).all().order_by('created')[0:1]
        return all_games[0] if len(all_games) else None
