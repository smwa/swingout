from django.shortcuts import render
from django.http import JsonResponse

from .models import Community, Style, Contact

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
        for tuples in Style.STYLES:
            if tuples[0] == style.style:
                styles.append(tuples[1])

    return {
        'uuid': community.uuid,
        'label': community.label,
        'latitude': community.latitude,
        'longitude': community.longitude,
        'url': community.url,
        'styles': styles,
    }
