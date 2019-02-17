from django.shortcuts import render

def index(request):
    return render(request, 'codenamez/index.html', {})

def user_login(request):
    return render(request, 'codenamez/index.html', {})

def user_logout(request):
    return render(request, 'codenamez/index.html', {})
