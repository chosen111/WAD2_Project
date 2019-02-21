import json, uuid, time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth.models import User
from codenamez.models import UserProfile, Chat, PrivateMessage, Game, GameList

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request):
    response = { }
    try:
        gameList = GameList.objects.filter(user=request.user)
        for game in gameList:
            game = game.game

            if game.cancelled or game.ended:
                continue

            response['game'] = {
                'id': str(game.id),
                'name': game.name,
                'created': game.created,
                'started': game.started
            }
            break
    except (TypeError, AttributeError, Exception):
        pass
            
    return render(request, 'codenamez/index.html', response)

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
                response['error'] = "Your account is disabled"
        else:
            response['error'] = "The username or password is invalid!"
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

def show_profile(request, profileId):
    response = { }
    try:
        user = User.objects.get(id=profileId)
        userProfile = UserProfile.objects.get(user=user)
        response = {
            'userProfile': userProfile,
        }
    except UserProfile.DoesNotExist:
        response['error'] = user.username + " does not have a profile set yet!"
    except User.DoesNotExist:
        response['error'] = "Profile with the id " + profileId + " does not exist!"

    return render(request, 'codenamez/profile.html', response)

@login_required
def show_game(request, gameId):
    response = { }
    #try:
        #game = Game.objects.get(id=uuid.UUID(gameId))
        #is_playing = GameList.objects.get(user=request.user, game=game)

        #response = {
        #    'game': game,
        #}
    #except (Game.DoesNotExist, ValueError):
        #response['error'] = "The game you are trying to access does not exist!"
    #except GameList.DoesNotExist:
        #response['error'] = "You are not currently invited to play in " + game.name
        
    return render(request, 'codenamez/game.html', response)