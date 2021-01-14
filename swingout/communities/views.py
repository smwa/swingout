from uuid import uuid4
from json import loads as loadJson

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from events.service import create as createEvent

from .models import Community, Style, Contact

# TODO Handle update requests, maybe in different django app

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)

def post(request):
    data = {
        'uuid': uuid4(),
        'label': request.POST.get('label'),
        'latitude': request.POST.get('latitude'),
        'longitude': request.POST.get('longitude'),
        'url': request.POST.get('url'),
        'styles': loadJson(request.POST.get('styles')),
        'contacts': loadJson(request.POST.get('contacts')),
    }
    # TODO! Validate data
    createEvent('AddCommunity', data)

def get(request):
    communities = []
    try:
        communityObjects = Community.objects.all()
    except Community.DoesNotExist:
        communityObjects = []
    for community in communityObjects:
        communities.append(__communityToDict(community))
    return JsonResponse(communities, safe=False)

def __communityToDict(community: Community):
    styles = []
    try:
        styleObjects = Style.objects.filter(community=community)
    except Style.DoesNotExist:
        styleObjects = []
    for style in styleObjects:
        styles.append(style.style)

    return {
        'uuid': community.uuid,
        'label': community.label,
        'latitude': community.latitude,
        'longitude': community.longitude,
        'url': community.url,
        'styles': styles,
    }
