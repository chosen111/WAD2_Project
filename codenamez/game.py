from django.core.cache import cache
from codenamez.models import UserProfile, Chat, PrivateMessage, Game, GamePlayer, WordList

from random import randint

from channels.db import database_sync_to_async

import time

class Error(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code

def isPlaying(player, game=None):
    playingGames = GamePlayer.objects.filter(player=player)
    for game in playingGames:
        game = game.game

        if game.cancelled or game.ended:
            continue
        
        data = {
            'id': str(game.id),
            'name': game.name,
            'owner': game.owner,
            'max_players': game.max_players,
            'created': game.created,
            'started': game.started
        }
        return data
    return False

@database_sync_to_async
def removePlayerFromGame(game_id, player):
    game = Game.objects.get(id=uuid.UUID(game_id))
    GamePlayer.objects.filter(game=game, player=request.user).delete()

#def generateCards(orange, purple, assassin=1, cards=25):
#    result = { }
#
#    wordList = WordList.objects.all()
#    words = []
#    for i in range(cards):
#        do {
#             tmp = randint(0, len(WordList))
#        }
#        while (wordList[tmp].word in words)

#def create(owner, name, password=None, max_players=6, data={})
#
#owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#    name = models.CharField(max_length=128)
#    password = models.CharField(max_length=128, editable=False, null=True, blank=True)
#    max_players = models.IntegerField()
#    data = models.TextField(default='{}')
#    history = models.TextField(default='null')
#    created = models.FloatField(default=time.time)
#    started = models.FloatField(null=True, blank=True)    
#    ended = models.FloatField(null=True, blank=True)
#    cancelled = models.BooleanField(default=False)
