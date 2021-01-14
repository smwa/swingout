from time import sleep

from django.core.management.base import BaseCommand

from events.service import get
from communities.models import Community, Style, Contact

SECONDS_BETWEEN_QUERIES = 10

class Command(BaseCommand):
    help = 'Loads events and updates the database'

    def handle(self, *args, **options):
        while True:
            for event in get(since=-1): # TODO! Keep track of last seen event
                if event.name == 'AddCommunity':
                    addCommunity(event)
                # TODO Add more event handling:
                # CommunityVerified(uuid, methods(like urls, emailAddresses, or phoneNumbers))
                # CommunityFailedVerification(uuid, methods)
                # CommunityUpdated(uuid, <community fields>)
                # CommunityUpdateRequested(uuid, message)
            sleep(SECONDS_BETWEEN_QUERIES)
    
def addCommunity(event):
    c = Community()
    c.label = event.data.label
    c.latitude = event.data.latitude
    c.longitude = event.data.longitude
    c.uuid = event.data.uuid
    c.url = event.data.url
    c.save()
    for styleName in event.data.styles:
        style = Style()
        style.community = c
        style.style = styleName
        style.save()
    for contactData in event.data.contacts:
        contact = Contact()
        contact.community = c
        if 'emailAddress' in contactData:
            contact.emailAddress = contactData.emailAddress
        if 'phoneNumber' in contactData:
            contact.phoneNumber = contactData.phoneNumber
        if 'url' in contactData:
            contact.url = contactData.url
        contact.save()
