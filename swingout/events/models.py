from django.db import models

class CanNotUpdateImmutableModelError(Exception):
    pass

class Event(models.Model):
    timeAdded = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    data = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.pk is None:
            return super(Event, self).save(*args, **kwargs)
        raise CanNotUpdateImmutableModelError("Cannot update event because it is immutable")

    def __str__(self):
        return '({}) {}'.format(self.id, self.name)
