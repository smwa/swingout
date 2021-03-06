from uuid import uuid4
import json

import phonenumbers

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, EmailValidator
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from i18n_discoverer.translation import gettext as _

from eventer.service import create as createEvent

from .models import Community, Style, Contact, UpdateRequest
from .forms import AddCommunityForm, RequestCommunityUpdateForm, UpdateCommunityForm

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

def thankYou(request, uuid):
    return render(request, 'communities/thankYou.html', {'timeOut': SECONDS_BETWEEN_QUERIES, 'uuid': uuid})

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
            for contactId in ['One', 'Two']:
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
                    try:
                        parsed_phone_number = phonenumbers.parse(value)
                        assert phonenumbers.is_possible_number(parsed_phone_number)
                        assert phonenumbers.is_valid_number(parsed_phone_number)
                    except Exception as e:
                        print("Found invalid phone number, details:", e, value)
                        form.add_error(valueField, _('Invalid Phone Number. Make sure to include the plus sign(+) and the country code, as in the example below.'))
                        return render(request, 'communities/addCommunity.html', {'form': form})
                    contacts.append(contact)
            data['contacts'] = contacts
            request.session['addCommunityData'] = json.dumps(data)
            return HttpResponseRedirect(reverse('communities:addPreview'))
    else:
        form = AddCommunityForm()

    return render(request, 'communities/addCommunity.html', {'form': form})

def update(request, uuid):
    if not request.user.has_perm('communities.change_community'):
        return HttpResponseForbidden(_('You do not have access to update communities'))
    community = Community.objects.get(uuid=uuid)
    if request.method == 'POST':
        form = UpdateCommunityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['uuid'] = community.uuid

            contacts = []
            for contactId in ['One', 'Two']:
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
                    try:
                        parsed_phone_number = phonenumbers.parse(value)
                        assert phonenumbers.is_possible_number(parsed_phone_number)
                        assert phonenumbers.is_valid_number(parsed_phone_number)
                    except Exception as e:
                        print("Found invalid phone number, details:", e, value)
                        form.add_error(valueField, _('Invalid Phone Number. Make sure to include the plus sign(+) and the country code, as in the example below.'))
                        return render(request, 'communities/addCommunity.html', {'form': form})
                    contacts.append(contact)
            data['contacts'] = contacts

            createEvent('CommunityUpdated', data)
            return HttpResponseRedirect(reverse('communities:thankYou', args=[data['uuid']]))
    else:
        contacts = community.contact_set.all()
        contactOneType = ''
        contactOne = ''
        if len(contacts) >= 1:
            contactOneType = 'emailAddress'
            contactOne = contacts[0].emailAddress
            if contacts[0].phoneNumber:
                contactOneType = 'phoneNumber'
                contactOne = contacts[0].phoneNumber
            if contacts[0].url:
                contactOneType = 'url'
                contactOne = contacts[0].url
        contactTwoType = ''
        contactTwo = ''
        if len(contacts) >= 2:
            contactTwoType = 'emailAddress'
            contactTwo = contacts[1].emailAddress
            if contacts[1].phoneNumber:
                contactTwoType = 'phoneNumber'
                contactTwo = contacts[1].phoneNumber
            if contacts[1].url:
                contactTwoType = 'url'
                contactTwo = contacts[1].url
        form = UpdateCommunityForm({
            'label': community.label,
            'structure': community.structure,
            'url': community.url,
            'latitude': community.latitude,
            'longitude': community.longitude,
            'styles': [style.style for style in community.style_set.all()],
            'contactOneType': contactOneType,
            'contactOne': contactOne,
            'contactTwoType': contactTwoType,
            'contactTwo': contactTwo,
        })

    return render(request, 'communities/updateCommunity.html', {'form': form})

def add_preview(request):
    data = json.loads(request.session.get('addCommunityData', {}))
    if request.method == 'POST':
        createEvent('CommunityAdded', data)
        del request.session['addCommunityData']
        return HttpResponseRedirect(reverse('communities:thankYou', args=[data['uuid']]))
    community = Community()
    community.label = data['label']
    community.url = data['url']
    return render(request, 'communities/addPreview.html', {
        'community': community,
        'url_formatted': community.url.replace('http://', '').replace('https://', ''),
        'styles': data['styles'],
    })

def markUpdateRequestHandled(request, uuid):
    request = UpdateRequest.objects.get(uuid=uuid)
    data = {
        'uuid': request.uuid
    }
    createEvent('CommunityUpdateRequestHandled', data)
    return JsonResponse({'Success': True})

def delete(request, uuid):
    if not request.user.has_perm('communities.delete_community'):
        return HttpResponseForbidden(_('You do not have access to delete communities'))
    community = Community.objects.get(uuid=uuid)
    data = {
        'uuid': community.uuid
    }
    createEvent('CommunityDeleted', data)
    return JsonResponse({'Success': True})

def requestUpdate(request, uuid):
    community = Community.objects.get(uuid=uuid)
    if request.method == 'POST':
        form = RequestCommunityUpdateForm(request.POST)
        if form.is_valid() and community is not None:
            data = form.cleaned_data
            data['community_uuid'] = community.uuid
            data['uuid'] = str(uuid4())
            createEvent('CommunityUpdateRequested', data)
            return HttpResponseRedirect(reverse('communities:thankYou', args=[community.uuid]))
    else:
        form = RequestCommunityUpdateForm()
    return render(request, 'communities/requestUpdate.html', {'form': form, 'label': community.label})

def map(request):
    return render(request, 'communities/map.html', {})

def manifest(request):
    return render(request, 'communities/manifest.json', {}, content_type='application/json')

def serviceWorker(request):
    return render(request, 'communities/service-worker.js', {}, content_type='application/javascript')

def __communityToDict(community: Community):
    styles = []
    try:
        styleObjects = Style.objects.filter(community=community)
    except Exception:
        styleObjects = []
    for style in styleObjects:
        styles.append(_(style.style))

    return {
        'uuid': community.uuid,
        'label': community.label,
        'latitude': community.latitude,
        'longitude': community.longitude,
        'url': community.url,
        'structure': _(community.structure),
        'styles': styles,
    }

def __fieldErrorResponse(field, message):
    return JsonResponse({
        "errors": [{'field': field, 'message': _(message)}]
    }, status=400)
