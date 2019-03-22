import json, uuid, time, re

# HTTP
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Database
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from codenamez.models import *
from codenamez.serializers import *
from django.core import serializers

# Channels
import pusher
pusher_client = pusher.Pusher(
  app_id='739753',
  key='f7e0c5de422f69bb8d14',
  secret='b3d1c2c684d929fa8672',
  cluster='eu',
  ssl=True
)
#from channels.db import database_sync_to_async
#from channels.layers import get_channel_layer
#from asgiref.sync import async_to_sync

# Utility
import codenamez.game as gameUtils

def index(request):
    response = { }
    #s = Session.objects.get(pk=request.session.session_key)
    # Find if there is any active game for the user
    if not request.user.is_anonymous:
        alreadyPlaying = gameUtils.isPlaying(request.user)
        if alreadyPlaying is not False:
            response["game"] = alreadyPlaying
            game = Game.objects.get(id=alreadyPlaying['id'])
            players = GamePlayer.objects.filter(game=game)
            response["game"]["players"] = players
            response["game"]["player_count"] = len(players)
    return render(request, 'codenamez/index.html', response)
    
def about(request):
    response = {}
    response = render(request, 'codenamez/about.html', context=response )
    return response

def how_to_play(request):
    response = {}
    response = render(request, 'codenamez/howtoplay.html', context=response)
    return response

def contact_us(request):
    response = {}
    response = render(request, 'codenamez/contactus.html', context=response)
    return response

def faq(request):
    response = {}
    response = render(request, 'codenamez/faq.html', context=response)
    return response

def user_register(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        ipaddress = get_client_ip(request)
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
        except IntegrityError as e:
            add_error_to_form(response, "username", "E_USERNAME_EXISTS")
        else:
            profile = UserProfile(user=user, ipaddress=ipaddress)
            profile.save()
    else:
        return HttpResponseRedirect(reverse('index'))
    return JsonResponse(response)

def user_login(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                response['redirect'] = reverse('index')
            else:
                add_error_to_form(response, "username", "E_AUTH_DISABLED")
        else:
            add_error_to_form(response, "username", "E_AUTH_MISMATCH")
            add_error_to_form(response, "password", "E_AUTH_MISMATCH")
    else:
        return HttpResponseRedirect(reverse('index'))
    return JsonResponse(response)

@login_required
def user_logout(request):
    response = {}
    if request.method == 'POST':
        logout(request)
        response['redirect'] = reverse('index')
    else:
        return HttpResponseRedirect(reverse('index'))
    return JsonResponse(response)

@login_required
def create_game(request):
    response = {}
    if request.method == 'POST':
        owner = request.user
        name = request.POST.get('name')
        players = request.POST.get('players')
        password = request.POST.get('password')
    
        # Check if the player is in an active game
        alreadyPlaying = gameUtils.isPlaying(owner)
        if alreadyPlaying is not False:
            add_error_to_notification(response, "E_ALREADY_PLAYING")
        else:
            # Player is not in any game, try to create and join the game
            game = Game(owner=owner, name=name, max_players=players) # todo: add password field
            game.save()

            player = GamePlayer(game=game, user=owner, joined=time.time(), is_admin=True)
            player.save()

            response['redirect'] = reverse('show_game', args=[game.id])
    else:
        return HttpResponseRedirect(reverse('index'))
    return JsonResponse(response)

@login_required
def join_game(request):
    response = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        try:
            game = Game.objects.get(id=uuid.UUID(id))
            response['redirect'] = reverse('show_game', args=[game.id])
        except (Game.DoesNotExist, ValueError):
            add_error_to_form(response, "id", "E_GAME_NOT_FOUND")
    else:
        return HttpResponseRedirect(reverse('index'))
    return JsonResponse(response)

@login_required
def lock_turn(request):
    response = { }
    if request.method == 'POST':
        try:
            game_id = request.POST.get('gameId')
            try:
                game = Game.objects.get(id=uuid.UUID(game_id))
                player = GamePlayer.objects.get(game=game, user=request.user)

                # Check if its supposed to be their turn
                if game.current_team != player.team:
                    raise gameUtils.GameError("E_NOT_YOUR_TURN")
                # Check if the game is not started yet
                if game.started is None or game.ended is not None:
                    raise gameUtils.GameError("E_GAME_NOT_IN_PROGRESS")
                # Check if they locked in their turn
                if player.locked_in:
                    raise gameUtils.GameError("E_TURN_CONFIRMED")
                
                # If the player that locked in their turn is a spymaster
                if player.is_spymaster:
                    # Attempt to set the new clue
                    gameUtils.lockClue(game, player, request.POST.get('clue'))
                    
                    response = {
                        'player': GamePlayerSerializer(player).data,
                        'clue': request.POST.get('clue')
                    }
                    pusher_client.trigger('game=' + game_id, 'player_locked_in', response)
                # If the player is not
                else:
                    cards = json.loads(game.cards)
                    # Attempt to lock in the cards
                    gameUtils.lockCards(game, player, cards, request.POST.get('selected'))
                    response = {
                        'player': GamePlayerSerializer(player).data,
                        'selected': request.POST.get('selected')
                    }
                    pusher_client.trigger('game=' + game_id, 'player_locked_in', response)
                    players = GamePlayer.objects.filter(game=game)
                    # Verify if everyone has locked in (finished their turn)
                    if gameUtils.isRoundFinished(game, players):
                        # Confirm the locked cards depending on which got the most selections
                        gameUtils.confirmCards(game, cards, players)
                        # Verify if the win condition has been met after this round
                        gameUtils.checkWinCondition(game, cards, players)

                        # Update player objects from database
                        player = GamePlayer.objects.get(game=game, user=request.user)
                        response['player'] = GamePlayerSerializer(player).data

                        pusher_client.trigger('game=' + game_id, 'game_round_end', {
                            'game': GameSerializer(game).data,
                            'player': GamePlayerSerializer(player).data,
                        })
            except (Game.DoesNotExist, ValueError):
                raise gameUtils.GameError("E_GAME_NOT_FOUND")
            except GamePlayer.DoesNotExist:
                raise gameUtils.GameError("E_NOT_PLAYING")
        except gameUtils.GameError as e:
            response['error'] = e.code
        finally:
            return JsonResponse(response)
    # Redirect if going manually to the link
    return HttpResponseRedirect(reverse('index'))

@login_required
def cancel_game(request):
    response = { }
    if request.method == 'POST':
        try:
            game_id = request.POST.get('gameId')
            try:
                game = Game.objects.get(id=uuid.UUID(game_id))
                player = GamePlayer.objects.get(game=game, user=request.user)
                
                if not player.is_admin:
                    raise gameUtils.GameError("E_NOT_ENOUGH_PRIV")
                if game.ended:
                    raise gameUtils.GameError("E_GAME_ENDED")

                #create the game
                gameUtils.cancelGame(game)
                pusher_client.trigger('game=' + game_id, 'game_cancelled', {
                    'game': GameSerializer(game).data,
                })

            except (Game.DoesNotExist, ValueError):
                raise gameUtils.GameError("E_GAME_NOT_FOUND")
            except GamePlayer.DoesNotExist:
                raise gameUtils.GameError("E_NOT_PLAYING")
        except gameUtils.GameError as e:
            response['error'] = e.code
        finally:
            return JsonResponse(response)
    # Redirect if going manually to the link
    return HttpResponseRedirect(reverse('index'))

@login_required
def start_game(request):
    response = { }
    if request.method == 'POST':
        try:
            game_id = request.POST.get('gameId')
            try:
                game = Game.objects.get(id=uuid.UUID(game_id))
                player = GamePlayer.objects.get(game=game, user=request.user)
                players = GamePlayer.objects.filter(game=game)

                if len(players) < 4:
                    raise gameUtils.GameError("E_NOT_ENOUGH_PLAYERS")
                if len(players) < game.max_players:
                    raise gameUtils.GameError("E_GAME_NOT_FULL")
                if len(list(filter(lambda player: player.team == 0, players))):
                    raise gameUtils.GameError("E_PLAYERS_NO_TEAM")
                if game.started:
                    raise gameUtils.GameError("E_GAME_IN_PROGRESS")

                #create the game
                gameUtils.createGame(game, players)
                pusher_client.trigger('game=' + game_id, 'game_started', {
                    'game': GameSerializer(game).data,
                    'players': GamePlayerSerializer(players, many=True).data,
                })

            except (Game.DoesNotExist, ValueError):
                raise gameUtils.GameError("E_GAME_NOT_FOUND")
            except GamePlayer.DoesNotExist:
                raise gameUtils.GameError("E_NOT_PLAYING")
        except gameUtils.GameError as e:
            response['error'] = e.code
        finally:
            return JsonResponse(response)
    # Redirect if going manually to the link
    return HttpResponseRedirect(reverse('index'))

@login_required
def switch_team(request):
    response = { }
    if request.method == 'POST':
        try:
            game_id = request.POST.get('gameId')
            team = request.POST.get('team')
            try:
                game = Game.objects.get(id=uuid.UUID(game_id))
                player = GamePlayer.objects.get(game=game, user=request.user)

                if player.team == team:
                    raise gameUtils.GameError("E_SAME_TEAM")

                player.team = team
                player.save()

                response = {
                    'player': GamePlayerSerializer(player).data
                }
                pusher_client.trigger('game=' + game_id, 'player_switched_team', response)
            except (Game.DoesNotExist, ValueError):
                raise gameUtils.GameError("E_GAME_NOT_FOUND")
            except GamePlayer.DoesNotExist:
                raise gameUtils.GameError("E_NOT_PLAYING")
        except gameUtils.GameError as e:
            response['error'] = e.code
        finally:
            return JsonResponse(response)
    # Redirect if going manually to the link
    return HttpResponseRedirect(reverse('index'))

@login_required
def connect_game(request):
    response = { }
    if request.method == 'POST':
        game_id = request.POST.get('id')
        try:
            # Check if the player is in an active game thats different from the current one
            alreadyPlaying = gameUtils.isPlaying(request.user)
            if alreadyPlaying is not False and alreadyPlaying['id'] != game_id:
                raise gameUtils.GameError("E_ALREADY_PLAYING")
            else:
                joined = time.time()
                # Player is not in any game, try to join the game
                try: 
                    game = Game.objects.get(id=uuid.UUID(game_id))
                    players = GamePlayer.objects.filter(game=game)
                    playing = GamePlayer.objects.get(game=game, user=request.user)     
                # The game is invalid or the value found in url is invalid
                except (Game.DoesNotExist, ValueError):
                    raise gameUtils.GameError("E_GAME_NOT_FOUND")
                # The user is not a player of this game yet... checking if allowed to participate
                except GamePlayer.DoesNotExist:
                    if game.started != None:
                        raise gameUtils.GameError("E_GAME_IN_PROGRESS")
                    if len(players) >= game.max_players:
                        raise gameUtils.GameError("E_GAME_FULL")

                    # Add player to the game
                    playing = GamePlayer(game=game, user=request.user, joined=joined)
                    playing.save()

                    players = GamePlayer.objects.filter(game=game)
                    # Repopulate the players result

                if game.cancelled:
                    raise gameUtils.GameError("E_GAME_CANCELLED")

                # Notify everyone a player has joined the game
                pusher_client.trigger('game=' + game_id, 'player_joined_game', {
                    'player': GamePlayerSerializer(playing).data,
                })
                # Prepare the response to send it back to the player
                response = {
                    'game': GameSerializer(game).data,
                    'player': GamePlayerSerializer(playing).data,
                    'players': GamePlayerSerializer(players, many=True).data
                }
        except gameUtils.GameError as e:
            response['error'] = e.code
        finally:
            return JsonResponse(response)
    # Redirect if going manually to the link
    return HttpResponseRedirect(reverse('index'))

@login_required
def show_game(request, game_id):
    return render(request, 'codenamez/game.html', { })

@login_required
def leave_game(request, game_id):
    response = {}
    try:
        game = Game.objects.get(id=uuid.UUID(game_id))
        playing = GamePlayer.objects.get(game=game, user=request.user)

        # Notify everyone a player has joined the game
        pusher_client.trigger('game=' + game_id, 'player_left_game', {
            'player': GamePlayerSerializer(playing).data,
        })
        playing.delete()
    except (Game.DoesNotExist, ValueError):
        pass
    except GamePlayer.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('index'))

def show_profile(request, profile_id):
    response = { }
    try:
        user = User.objects.get(id=profile_id)
        userProfile = UserProfile.objects.get(user=user)
        response = {
            'userProfile': userProfile,
        }
    except UserProfile.DoesNotExist:
        response['error'] = user.username + " does not have a profile set yet!"
    except User.DoesNotExist:
        response['error'] = "Profile with the id " + profile_id + " does not exist!"
    return render(request, 'codenamez/profile.html', response)

# Utility functions
def add_error_to_form(obj, id, error):
    if "error" not in obj: obj["error"] = { }
    if "form" not in obj["error"]: obj["error"]["form"] = { }
    obj["error"]["form"][id] = error

def add_error_to_notification(obj, error):
    if "error" not in obj: obj["error"] = { }
    obj["error"]["notification"] = error

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
