from django.core.management.base import BaseCommand

from communities.models import Community, EventCounter


class Command(BaseCommand):
    help = 'Clears database and event counter'

    def handle(self, *args, **options):
        try:
            for c in Community.objects.all():
                c.delete()
        except Exception:
            pass
        try:
            for ec in EventCounter.objects.all():
                ec.delete()
        except Exception:
            pass
