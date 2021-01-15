from time import sleep

from django.core.management.base import BaseCommand

from events.service import get
from communities.models import Community, Style, Contact, EventCounter

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
            for event in get(since=eventCounter.lastSeen):
                eventCounter.lastSeen = event.id
                eventCounter.save()
                if event.name == 'CommunityAdded':
                    addCommunity(event)
                # TODO Add more event handling:
                # CommunityVerified(uuid, methods(like urls, emailAddresses, or phoneNumbers))
                # CommunityFailedVerification(uuid, methods)
                # CommunityUpdated(uuid, <community fields>)
            sleep(SECONDS_BETWEEN_QUERIES)
    
def addCommunity(event):
    c = Community()
    c.label = event.data['label']
    c.latitude = event.data['latitude']
    c.longitude = event.data['longitude']
    c.uuid = event.data['uuid']
    c.url = event.data['url']
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
