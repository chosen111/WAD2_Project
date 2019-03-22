from django.core.cache import cache
from codenamez.models import *

from random import randint

import time, json, re

class GameError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code

def isPlaying(player, game=None):
    playingGames = GamePlayer.objects.filter(user=player)
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

def cancelGame(game):
    game.cancelled = True
    game.save()

def createGame(game, players):
    game.current_team = randint(1, 2)
    game.current_round = 1
    game.cards = json.dumps(randomCards(game.current_team))
    game.started = time.time()

    game.save()
    randomSpymaster(players)

def randomSpymaster(players):
    orangeTeam = list(filter(lambda player: player.team == 1, players))
    purpleTeam = list(filter(lambda player: player.team == 2, players))

    randomOrange = randint(0, len(orangeTeam)-1)
    orangeTeam[randomOrange].is_spymaster = True
    orangeTeam[randomOrange].save()

    randomPurple = randint(0, len(purpleTeam)-1)
    purpleTeam[randomPurple].is_spymaster = True
    purpleTeam[randomPurple].save()

def randomCards(startingTeam, orangeCards=5, purpleCards=5, assassinCards=1, totalCards=25):
    wordList = WordList.objects.all()
    words = []
    
    cardTypes = [0, 1, 2, 5]
    assignedTypes = {
        0: { "current": 0, "maximum": assassinCards }, # Assassin
        1: { "current": 0, "maximum": orangeCards }, # Orange Team
        2: { "current": 0, "maximum": purpleCards }, # Purple Team
    }
    # Starting team gets an extra card to guess
    assignedTypes[startingTeam]['maximum'] += 1 
    assignedTypes[5] = { "current": 0, "maximum": totalCards-assignedTypes[0]['maximum']-assignedTypes[1]['maximum']-assignedTypes[2]['maximum'] } # Bystanders

    currentCards = []
    for i in range(totalCards):
        cardWord = getRandomWord(wordList, words)
        cardType = getRandomType(assignedTypes, cardTypes)

        currentCards.append({
            "selected": 0,
            "type": cardType,
            "word": cardWord
        })
    return currentCards

def getRandomWord(wordList, words):
    cardWord = wordList[randint(0, len(wordList)-1)].word
    while (cardWord in words):
        cardWord = wordList[randint(0, len(wordList)-1)].word
    words.append(cardWord)

    return cardWord

def getRandomType(assignedTypes, cardTypes):
    cardType = cardTypes[randint(0, len(cardTypes)-1)]
    while (assignedTypes[cardType]["current"] >= assignedTypes[cardType]["maximum"]):
        cardType = cardTypes[randint(0, len(cardTypes)-1)]
    assignedTypes[cardType]["current"] += 1

    return cardType

def isRoundFinished(game, players):
    playingTeam = list(filter(lambda player: player.team == game.current_team, players))
    for player in playingTeam:
        if player.locked_in is not True:
            return False
    return True

def checkWinCondition(game, cards, players):
    assassinCards = list(filter(lambda card: card['type'] == 0, cards))
    orangeCards = list(filter(lambda card: card['type'] == 1, cards))
    purpleCards = list(filter(lambda card: card['type'] == 2, cards))
    
    for card in assassinCards:
        if "guess" in card:
            return wonGame(game, getOppositeTeam(card['guess']))
    
    orangeHit = 0
    purpleHit = 0
    for card in orangeCards:
        if "guess" in card:
            orangeHit += 1
    
    for card in purpleCards:
        if "guess" in card:
            purpleHit += 1

    orangeWon = (orangeHit == len(orangeCards))
    purpleWon = (purpleHit == len(purpleCards))

    # Draw game
    if orangeWon and orangeWon == purpleWon:
        return wonGame(game)
    else:
        # Orange Team won
        if orangeWon:
            return wonGame(game, 1)
        # Purple Team won
        if purpleWon:
            return wonGame(game, 2)

    # If no one won just end the round
    
    endRound(game)

def wonGame(game, team=0):
    game.winner = team
    endGame(game)

def endGame(game):
    game.ended = time.time()
    game.save()

def endRound(game):
    game.current_round += 1
    game.current_team = getOppositeTeam(game.current_team)
    game.current_clue = '{}'
    game.save()
    
def lockCards(game, player, cards, selected):
    if selected is not None:
        selected = json.loads(selected)
        isCardGuessed(cards, selected)

    # Lock in the player's turn
    lockPlayer(player)

    game.cards = json.dumps(cards)
    game.save()

def isCardGuessed(cards, selected):
    for i in selected:
        if "guess" in cards[i]:
            raise GameError("E_CARD_ALREADY_REVEALED")
        else:
            cards[i]['selected'] += 1

def confirmCards(game, cards, players):
    # Find the highest selection starting from 1 to make sure we don't select all the cards if no one selected any
    highest = 1
    for card in cards:
        if card['selected'] > highest:
            highest = card['selected']
    
    # Filter and loop through all the cards that don't have the highest number of selection
    finalCards = list(filter(lambda card: card['selected'] == highest, cards))
    for card in finalCards:
        card['guess'] = game.current_team

    
    # Reset the selected counter
    for card in cards:
        card['selected'] = 0
    
    # Unlock the players that locked in their turn
    unlockPlayers(players)
    
    # Save the updated cards
    game.cards = json.dumps(cards)
    game.save()

def lockClue(game, player, clue):
    if clue is None:
        raise GameError("E_CLUE_INVALID")

    current_clue = json.loads(game.current_clue)
    # The clue has already been set for this turn
    if "word" in current_clue:
        raise GameError("E_CLUE_ALREADY_SET")

    clue = json.loads(clue)
    # Check if the clue is correctly formatted
    clue['word'] = re.sub(r'\W+', ' ', clue['word'])
    if len(clue['word'].split()) > 1:
        raise GameError("E_CLUE_INVALID")

    # Check if the clue word has more than 3 characters
    if len(clue['word']) <= 3:
        raise GameError("E_CLUE_RANGE")

    # Check if the the clue number is actually a number between 0 and 5
    try:
        clue['num'] = int(clue['num'])
        if 0 <= clue['num'] <= 5:
            pass
        else:
            raise GameError("E_CLUE_NUM_EXCEED")
    except ValueError:
        raise GameError("E_CLUE_NUM_NAN")

    # Lock in the player's turn
    lockPlayer(player)

    # Save the updated game
    game.current_clue = json.dumps(clue)
    game.save()

def unlockPlayers(players):
    for player in players:
        if player.locked_in:
            player.locked_in = False
            player.save()

def lockPlayer(player):
    player.locked_in = True
    player.save()

def getOppositeTeam(team):
    if team == 1: return 2
    if team == 2: return 1