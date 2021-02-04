from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import *

class UpdateRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('message', 'show_delete_url')
    fields = ('message', 'community', 'show_delete_url')

    def show_delete_url(self, obj):
        return format_html("<a target='_blank' href='{url}'>{uuid}</a>", url=reverse('communities:markUpdateRequestHandled', args=[obj.uuid]), uuid=obj.uuid)

    show_delete_url.short_description = "Delete URL"

admin.site.register(Community)
admin.site.register(Style)
admin.site.register(Contact)
admin.site.register(EventCounter)
admin.site.register(UpdateRequest, UpdateRequestAdmin)
