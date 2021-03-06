from django.db import models
from i18n_discoverer.translation import gettext as _

class Community(models.Model):
    UNINCORPORATED = 'Unincorporated'
    NON_PROFIT = 'Non-Profit'
    BUSINESS = 'Business'

    STRUCTURES = (
        (UNINCORPORATED, _(UNINCORPORATED)),
        (NON_PROFIT, _(NON_PROFIT)),
        (BUSINESS, _(BUSINESS)),
    )

    uuid = models.CharField(max_length=36)
    label = models.CharField(max_length=256)
    structure = models.CharField(max_length=16, choices=STRUCTURES, default=UNINCORPORATED)
    latitude = models.FloatField()
    longitude = models.FloatField()
    url = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = "Communities"
        indexes = [
            models.Index(fields=['uuid',]),
        ]

    def __str__(self):
        return "{} - {}".format(self.label, self.uuid)

class Style(models.Model):
    BALBOA = 'Balboa'
    BLUES = 'Blues'
    BOOGIE_WOOGIE = 'Boogie Woogie'
    CAROLINA_SHAG = 'Carolina Shag'
    CHARLESTON = 'Charleston'
    CHICAGO_STEPPING = "Chicago Steppin'"
    COLLEGIATE_SHAG = 'Collegiate Shag'
    EAST_COAST_SWING = 'East Coast Swing'
    FUSION = 'Fusion'
    LINDY_HOP = 'Lindy Hop'
    SAINT_LOUIS_SHAG = 'St. Louis Shag'
    WEST_COAST_SWING = 'West Coast Swing'

    __STYLES_LIST = [
        BALBOA,
        BLUES,
        BOOGIE_WOOGIE,
        CAROLINA_SHAG,
        CHARLESTON,
        CHICAGO_STEPPING,
        COLLEGIATE_SHAG,
        EAST_COAST_SWING,
        FUSION,
        LINDY_HOP,
        SAINT_LOUIS_SHAG,
        WEST_COAST_SWING,
    ]

    STYLES = tuple([(style, _(style)) for style in __STYLES_LIST])
    
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

class UpdateRequest(models.Model):
    message = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=36)

    def __str__(self):
        return '{}. {}'.format(self.id, self.community.label)
