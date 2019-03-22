import time, uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ipaddress = models.GenericIPAddressField()
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    options = models.TextField(default='null')
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    ranking = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created = models.FloatField(default=time.time)
    visible = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.message + ' by ' + self.user.username

class PrivateMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_pm_set")
    target = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="target_pm_set")
    message = models.TextField()
    created = models.FloatField(default=time.time)
    visible = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.message + ' by ' + self.user.username

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128, editable=False, null=True, blank=True)
    max_players = models.IntegerField()
    current_team = models.IntegerField(null=True, blank=True)
    current_round = models.IntegerField(null=True, blank=True)
    current_clue = models.CharField(max_length=128, default={})
    cards = models.TextField(default='{}')
    winner = models.IntegerField(null=True, blank=True)
    created = models.FloatField(default=time.time)
    started = models.FloatField(null=True, blank=True)    
    ended = models.FloatField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class GamePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    team = models.IntegerField(default=0)
    joined = models.FloatField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_spymaster = models.BooleanField(default=False)
    locked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ("game", "user")

    def __str__(self):
        return str(self.game.id) + "::" + self.user.username

class WordList(models.Model):
    word = models.CharField(max_length=128)

    def __str__(self):
        return self.word
