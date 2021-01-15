from django.shortcuts import render

def map(request):
    return render(request, 'public/map.html', {})

def addCommunity(request):
    return render(request, 'public/addCommunity.html', {})
