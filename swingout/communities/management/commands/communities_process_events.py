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
        while True:
            try:
                events = get(since=eventCounter.lastSeen)
                for event in events:
                    eventCounter.lastSeen = event.id
                    eventCounter.save()
                    if event.name == 'CommunityAdded':
                        addCommunity(event)
                    if event.name == 'CommunityUpdateRequested':
                        addUpdateRequest(event)
                    if event.name == 'CommunityUpdateRequestHandled':
                        removeUpdateRequest(event)
                    if event.name == 'CommunityDeleted':
                        removeCommunity(event)
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

def addUpdateRequest(event):
    community = Community.objects.filter(uuid=event.data['community_uuid'])[0]
    request = UpdateRequest()
    request.message = event.data['message']
    request.community = community
    request.uuid = event.data['uuid']
    request.save()

def removeUpdateRequest(event):
    request = UpdateRequest.objects.filter(uuid=event.data['uuid'])
    request.delete()

def removeCommunity(event):
    Community.objects.filter(uuid=event.data['uuid']).delete()
