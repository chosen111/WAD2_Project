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

def user_register(request):
    response = {}
    print("register")
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm-password')
        print(username)
        print(email)
        print(password)
        print(confirmPassword)

        #user_form = UserForm(data=request.POST)
        #profile_form = UserProfileForm(data=request.POST)

        #if user_form.is_valid() and profile_form.is_valid():
        #    user = user_form.save()
        #    user.set_password(user.password)
        #    user.save()

        #    profile = profile_form.save(commit=False)
        #    profile.user = user

        #    if 'picture' in request.FILES:
        #        profile.picture = request.FILES['picture']

        #    profile.save()
        #else:
        #    print(user_form.errors, profile_form.errors)
    else:
        return HttpResponseRedirect(reverse('index'))

    return JsonResponse(response)

    #context_dict = {
    #    'user_form': user_form,
    #    'profile_form': profile_form,
    #    'registered': registered,
    #}
    #return render(request, 'rango/register.html', context_dict)

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
                response['error'] = { 
                    'form': {
                        'username': "E_AUTH_DISABLED"
                    }
                }
        else:
            response['error'] = { 
                'form': {
                    'username': "E_AUTH_MISMATCH", 
                    'password': "E_AUTH_MISMATCH"
                }
            }
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