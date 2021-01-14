from uuid import uuid4
from json import loads as loadJson

import validators

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

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
        'latitude': int(request.POST.get('latitude')),
        'longitude': request.POST.get('longitude'),
        'url': request.POST.get('url'),
        'styles': list(loadJson(request.POST.get('styles'))),
        'contacts': list(loadJson(request.POST.get('contacts'))),
    }
    if data['label'] is None or data['label'] == '':
        return __fieldErrorResponse('label', 'Label cannot be empty')
    if data['latitude'] < 0.00001 and data['latitude'] > -0.00001:
        return __fieldErrorResponse('latitude', 'Latitude cannot be empty')
    if data['longitude'] < 0.00001 and data['longitude'] > -0.00001:
        return __fieldErrorResponse('longitude', 'Longitude cannot be empty')
    if not validators.url(data['url']):
        return __fieldErrorResponse('url', 'Valid URL required')
    if len(set(data.styles)) != len(data.styles) or len(data.styles) == 0:
        return __fieldErrorResponse('styles', 'Styles are required, and cannot contain duplicates')
    STYLES = [style[0] for style in Style.STYLES]
    for style in data.styles:
        if style not in STYLES:
            return __fieldErrorResponse('styles', 'Invalid style')
    if len(data['contacts']) < 1 or len(data['contacts']) > 5:
        return __fieldErrorResponse('contacts', 'You must have between 1 and 5 contacts')
    for contact in data['contacts']:
        if len(contact) > 1 or len(contact) < 1:
            return __fieldErrorResponse('contacts', 'Contacts can only contain one piece of information')
        if 'emailAddress' not in contact and 'phoneNumber' not in contact and 'url' not in contact:
            return __fieldErrorResponse('contacts', 'Contacts must have an email address, a phone number, or a url')
    createEvent('AddCommunity', data)

def get(request):
    communities = []
    try:
        communityObjects = Community.objects.all()
    except Community.DoesNotExist:
        communityObjects = []
    for community in communityObjects:
        communities.append(__communityToDict(community))
    return JsonResponse({"communities": communities})

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

def __fieldErrorResponse(field, message):
    return JsonResponse({
        "errors": [{'field': field, 'message': _(message)}]
    }, status=400)
