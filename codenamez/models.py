import time, uuid
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    game = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128, blank=True)
    players = models.TextField(default='players: {}')
    history = models.TextField(default='history: {}')
    created = models.IntegerField(default=time.time)
    started = models.IntegerField(null=True, blank=True)    
    ended = models.IntegerField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ipaddress = models.GenericIPAddressField()
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True)
    options = models.TextField(default='options: {}')

    def __str__(self):
        return self.user.username

