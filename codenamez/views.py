from django.shortcuts import render

def index(request):
    return render(request, 'codenamez/index.html', context_dict)
