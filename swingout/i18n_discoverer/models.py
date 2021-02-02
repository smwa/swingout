from django.db import models

class Message(models.Model):
    singular = models.TextField()
    plural = models.TextField(null=True)
    location = models.TextField(null=True)
    context = models.TextField(null=True)

    def __str__(self):
        return self.singular
