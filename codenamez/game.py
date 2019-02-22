from django.core.cache import cache
from codenamez.models import WordList

from random import randint

class GameError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code

game = {
    'connected_players': [],
}

def init():
    cache.add('games', {})

def connect(game, user):
    init()

    games = cache.get('games')
    games[game]['connected_players'] = test

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
