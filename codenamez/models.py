import time, uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ipaddress = models.GenericIPAddressField()
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    options = models.TextField(default='options: {}')

    def __str__(self):
        return self.user.username

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128, blank=True)
    max_players = models.IntegerField()
    history = models.TextField(default='history: {}')
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

    def __str__(self):
        return str(self.game)


