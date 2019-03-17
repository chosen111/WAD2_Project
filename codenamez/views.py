import json, uuid, time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth.models import User
from codenamez.models import UserProfile, Chat, PrivateMessage, Game, GameList

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.db import IntegrityError

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
    
def about(request):
    response = {}

    response = render(request, 'codenamez/about.html', context = response )
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
    response = render(request, 'codenamez/howtoplay.html', context = response )
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
    return render(request, 'codenamez/game.html', { })

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
