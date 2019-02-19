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
    userProfile = UserProfile.objects.get(user=User.objects.get(id=profileId))

    return render(request, 'codenamez/profile.html', response)

def show_game(request, gameId):
    response = { }            
    return render(request, 'codenamez/game.html', response)