from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    theUserWhoEarnedIt = models.OneToOneField(User, on_delete=models.CASCADE)
    theHighScore = models.IntegerField(default=0)
    theNumOfGamesPlayed = models.IntegerField(default=0)

    def __str__(self):
        return self.theUserWhoEarnedIt.username + " has a high score of " + str(self.theHighScore)
