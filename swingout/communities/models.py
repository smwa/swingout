from django.db import models

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
    STYLES = (
        (LINDY_HOP, LINDY_HOP),
        # TODO add more
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    style = models.CharField(
        max_length=32,
        choices=STYLES,
        default=LINDY_HOP
    )

class Contact(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    emailAddress = models.EmailField(default='')
    phoneNumber = models.CharField(default='', max_length=64)
    url = models.CharField(default='', max_length=512)

class EventCounter(models.Model):
    lastSeen = models.BigIntegerField(default=-1)
