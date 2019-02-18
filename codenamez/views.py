import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth.models import User
from codenamez.models import UserData
from codenamez.models import Game

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request):
    response = { }
    if request.user.is_authenticated:
        data = None
        try:
            data = UserData.objects.get(user=request.user)
            if request.user.userdata.game:
                try:
                    game = Game.objects.get(game=request.user.userdata.game.game)
                    response['game'] = {
                        'game': game.game,
                        'name': game.name,
                        'players': game.players,
                        'created': game.created,
                        'started': game.started
                    }
                except Game.DoesNotExist:
                    response['game'] = None
        except UserData.DoesNotExist:
            pass 
            
    return render(request, 'codenamez/index.html', response)

def user_login(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)
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
