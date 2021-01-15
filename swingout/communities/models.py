from django.db import models
from django.utils.translation import gettext as _

class Community(models.Model):
    uuid = models.CharField(max_length=36)
    label = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    url = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = "Communities"
        indexes = [
            models.Index(fields=['uuid',]),
        ]

    def __str__(self):
        return self.label

class Style(models.Model):
    LINDY_HOP = 'Lindy Hop'
    WEST_COAST_SWING = 'West Coast Swing'
    STYLES = (
        (LINDY_HOP, _(LINDY_HOP)),
        (WEST_COAST_SWING, _(WEST_COAST_SWING)),
        # TODO add more
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    style = models.CharField(
        max_length=32,
        choices=STYLES,
        default=LINDY_HOP
    )

    def __str__(self):
        return '{} - {}'.format(self.community.label, self.style)

class Contact(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    emailAddress = models.EmailField(default='')
    phoneNumber = models.CharField(default='', max_length=64)
    url = models.CharField(default='', max_length=512)

    def __str__(self):
        return '{} - {}{}{}'.format(self.community.label, self.emailAddress, self.phoneNumber, self.url)

class EventCounter(models.Model):
    lastSeen = models.BigIntegerField(default=-1)

    def __str__(self):
        return self.lastSeen
