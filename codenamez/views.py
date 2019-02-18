from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'codenamez/index.html', {})

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
        return render(request, 'codenamez/index.html', {})
    
    return JsonResponse(response)

@login_required
def user_logout(request):
    response = {}
    if request.method == 'POST':
        logout(request)
        response['redirect'] = reverse('index')
    else:
        return render(request, 'codenamez/index.html', {})
    
    return JsonResponse(response)
