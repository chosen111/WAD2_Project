import json, uuid, time

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
from codenamez.models import UserProfile, Chat, PrivateMessage, Game, GamePlayer
from django.core import serializers

# Channels
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Utility
import codenamez.game as gameUtil

def index(request):
    response = { }
    #s = Session.objects.get(pk=request.session.session_key)
    # Find if there is any active game for the user
    if not request.user.is_anonymous:
        alreadyPlaying = gameUtil.isPlaying(request.user)
        if alreadyPlaying is not False:
            response["game"] = alreadyPlaying
            players = GamePlayer.objects.filter(player=request.user)
            response["game"]["players"] = players
            response["game"]["player_count"] = len(players)
    return render(request, 'codenamez/index.html', response)
    
def about(request):
    response = {}

    response = render(request, 'codenamez/about.html', context=response )
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()


    # print out whether the method is a GET or a POST
    print(request.method)
    #print out the user name, if no one is logged in it prints 'AnonymousUser'
    print(request.user)
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
        alreadyPlaying = gameUtil.isPlaying(owner)
        if alreadyPlaying is not False:
            add_error_to_notification(response, "E_ALREADY_PLAYING")
        else:
            # Player is not in any game, try to create and join the game
            game = Game(owner=owner, name=name, max_players=players) # todo: add password field
            game.save()

            player = GamePlayer(game=game, player=owner, is_admin=True)
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
            game = Game.objects.get(id=uuid.UUID(id)) # todo: password check
            response['redirect'] = reverse('show_game', args=[game.id])
        except (Game.DoesNotExist, ValueError):
            add_error_to_form(response, "id", "E_GAME_NOT_FOUND")
    else:
        return HttpResponseRedirect(reverse('index'))
    return JsonResponse(response)

@login_required
def show_game(request, game_id):
    return render(request, 'codenamez/game.html', { })

@login_required
def leave_game(request, game_id):
    response = {}
    try:
        game = Game.objects.get(id=uuid.UUID(game_id))
        GamePlayer.objects.get(game=game, player=request.user).delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(game_id,
            {
                "type": "game.leave",
                "game": game_id,
                "player": request.user,
            }
        )
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
