import inspect
import os

from django.conf import settings
from django.utils.translation import *
from django.utils import translation as __translation

from .models import Message

__TRACK = bool(settings.I18N_DISCOVERER_TRACKING)

def gettext(message):
    if __TRACK:
        __save(message)
    return __translation.gettext(message)

def gettext_noop(message):
    if __TRACK:
        __save(message)
    return __translation.gettext_noop(message)

def ngettext(singular, plural, number=None):
    if __TRACK:
        __save(singular, plural)
    return __translation.ngettext(singular, plural, number)

def pgettext(context, message):
    if __TRACK:
        __save(message, None, context)
    return __translation.pgettext(context, message)

def npgettext(context, singular, plural, number=None):
    if __TRACK:
        __save(singular, plural, context)
    return __translation.npgettext(context, singular, plural, number)

def gettext_lazy(message):
    if __TRACK:
        __save(message)
    return __translation.gettext_lazy(message)

def ngettext_lazy(singular, plural, number=None):
    if __TRACK:
        __save(singular, plural)
    return __translation.ngettext_lazy(singular, plural, number)

def pgettext_lazy(context, message):
    if __TRACK:
        __save(message, None, context)
    return __translation.pgettext_lazy(context, message)

def npgettext_lazy(context, singular, plural, number=None):
    if __TRACK:
        __save(singular, plural, context)
    return __translation.npgettext_lazy(context, singular, plural, number)

def __save(singular, plural=None, context=None):
    caller = inspect.stack()[2]
    path = os.path.relpath(caller[1], '..')
    location = "{}:{}".format(path, caller[2])
    try:
        message = Message.objects.get(singular=singular, plural=plural, context=context, location=location)
    except Message.DoesNotExist:
        message = Message()
        message.singular = singular
        message.plural = plural
        message.context = context
        message.location = location
        message.save()
