from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'codenamez/index.html', {})

def user_login(request):
    return render(request, 'codenamez/index.html', {})

@login_required
def user_logout(request):
    logout(request)

    response = {
        'redirect': reverse('index')
    }
    return JsonResponse(response)
