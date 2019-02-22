import time, uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ipaddress = models.GenericIPAddressField()
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    options = models.TextField(default='null')

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
    data = models.TextField(default='{}')
    history = models.TextField(default='null')
    created = models.FloatField(default=time.time)
    started = models.FloatField(null=True, blank=True)    
    ended = models.FloatField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class GameList(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    team = models.CharField(max_length=32, blank=True)
    joined = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("game", "user")

    def __str__(self):
        return str(self.game.id)

class WordList(models.Model):
    word = models.CharField(max_length=128)

    def __str__(self):
        return self.word
