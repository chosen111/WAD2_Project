from django.core.cache import cache

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
