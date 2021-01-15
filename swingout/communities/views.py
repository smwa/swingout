from uuid import uuid4
from json import loads as loadJson

import validators

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, EmailValidator
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.translation import gettext as _

from events.service import create as createEvent

from .models import Community, Style, Contact
from .forms import AddCommunityForm, RequestCommunityUpdateForm

from .management.commands.communities_process_events import SECONDS_BETWEEN_QUERIES

def index(request):
    communities = []
    try:
        communityObjects = Community.objects.all()
    except Exception:
        communityObjects = []
    for community in communityObjects:
        communities.append(__communityToDict(community))
    return JsonResponse({"communities": communities})

def thankYou(request):
    return render(request, 'communities/thankYou.html', {'timeOut': SECONDS_BETWEEN_QUERIES})

def add(request, latitude=0.0, longitude=0.0):
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values.update({
            'latitude': latitude,
            'longitude': longitude,
        })
        form = AddCommunityForm(post_values)
        if form.is_valid():
            data = form.cleaned_data
            data['uuid'] = str(uuid4())

            contacts = []
            for contactId in ['One', 'Two', 'Three']:
                keyField = 'contact{}Type'.format(contactId)
                valueField = 'contact{}'.format(contactId)
                key = data[keyField]
                value = data[valueField]
                del data[keyField]
                del data[valueField]
                if value == '':
                    continue
                contact = {key: value}
                if key == 'emailAddress':
                    try:
                        EmailValidator()(value)
                        contacts.append(contact)
                    except ValidationError as e:
                        print("Found invalid email, details:", e, value)
                        form.add_error(valueField, _('Invalid email address'))
                        return render(request, 'communities/addCommunity.html', {'form': form})
                if key == 'url':
                    try:
                        URLValidator()(value)
                        contacts.append(contact)
                    except ValidationError as e:
                        print("Found invalid URL, details:", e, value)
                        form.add_error(valueField, _('Invalid URL'))
                        return render(request, 'communities/addCommunity.html', {'form': form})
                if key == 'phoneNumber':
                    # TODO Validate global phone numbers
                    contacts.append(contact)
            data['contacts'] = contacts
            createEvent('CommunityAdded', data)
            return HttpResponseRedirect(reverse('communities:addThankYou'))
    else:
        form = AddCommunityForm()

    return render(request, 'communities/addCommunity.html', {'form': form})

def requestUpdate(request, uuid):
    community = Community.objects.filter(uuid=uuid)[0]
    if request.method == 'POST':
        form = RequestCommunityUpdateForm(request.POST)
        if form.is_valid() and community is not None:
            data = form.cleaned_data
            data['uuid'] = community.uuid
            createEvent('CommunityUpdateRequested', data)
            return HttpResponseRedirect(reverse('communities:thankYou'))
    else:
        form = RequestCommunityUpdateForm()
    return render(request, 'communities/requestUpdate.html', {'form': form, 'label': community.label})

def __communityToDict(community: Community):
    styles = []
    try:
        styleObjects = Style.objects.filter(community=community)
    except Exception:
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
