from time import sleep

from django.core.management.base import BaseCommand

from eventer.service import get
from communities.models import Community, Style, Contact, EventCounter, UpdateRequest

SECONDS_BETWEEN_QUERIES = 10

class Command(BaseCommand):
    help = 'Loads events and updates the database'

    def handle(self, *args, **options):
        eventCounter = EventCounter()
        try:
            eventCounter = EventCounter.objects.all()[0]
        except IndexError:
            pass
        handlers = {
            'CommunityAdded': addCommunity,
            'CommunityUpdateRequested': addUpdateRequest,
            'CommunityUpdateRequestHandled': removeUpdateRequest,
            'CommunityDeleted': removeCommunity,
            'CommunityUpdated': updateCommunity,
        }
        while True:
            try:
                events = get(since=eventCounter.lastSeen)
                for event in events:
                    eventCounter.lastSeen = event.id
                    eventCounter.save()
                    if event.name in handlers:
                        handlers[event.name](event)
                if len(events) < 1:
                    sleep(SECONDS_BETWEEN_QUERIES)
            except Exception as e:
                print(e)

def addCommunity(event):
    c = Community()
    c.label = event.data['label']
    c.latitude = event.data['latitude']
    c.longitude = event.data['longitude']
    c.uuid = event.data['uuid']
    c.url = event.data['url']
    c.structure = event.data['structure']
    c.save()
    for styleName in event.data['styles']:
        style = Style()
        style.community = c
        style.style = styleName
        style.save()
    for contactData in event.data['contacts']:
        contact = Contact()
        contact.community = c
        if 'emailAddress' in contactData:
            contact.emailAddress = contactData['emailAddress']
        if 'phoneNumber' in contactData:
            contact.phoneNumber = contactData['phoneNumber']
        if 'url' in contactData:
            contact.url = contactData['url']
        contact.save()

def updateCommunity(event):
    community = Community.objects.get(uuid=event.data['uuid'])
    community.label = event.data['label']
    community.latitude = event.data['latitude']
    community.longitude = event.data['longitude']
    community.url = event.data['url']
    community.structure = event.data['structure']
    community.save()
    oldStyles = [style.style for style in community.style_set.all()]
    newStyles = event.data['styles']
    for style in oldStyles:
        if style not in newStyles:
            Style.objects.get(community=community, style=style).delete()
    for style in newStyles:
        if style not in oldStyles:
            style_model = Style()
            style_model.community = community
            style_model.style = style
            style_model.save()

def addUpdateRequest(event):
    community = Community.objects.get(uuid=event.data['community_uuid'])
    request = UpdateRequest()
    request.message = event.data['message']
    request.community = community
    request.uuid = event.data['uuid']
    request.save()

def removeUpdateRequest(event):
    UpdateRequest.objects.get(uuid=event.data['uuid']).delete()

def removeCommunity(event):
    Community.objects.get(uuid=event.data['uuid']).delete()
