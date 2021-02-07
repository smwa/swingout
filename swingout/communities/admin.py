from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import *

class UpdateRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('message', 'show_delete_url')
    fields = ('message', 'community', 'show_delete_url')

    def show_delete_url(self, obj):
        if not obj.uuid:
            return ''
        return format_html("<a target='_blank' href='{url}'>{uuid}</a>", url=reverse('communities:markUpdateRequestHandled', args=[obj.uuid]), uuid=obj.uuid)

    show_delete_url.short_description = "Delete URL"

class CommunityAdmin(admin.ModelAdmin):
    readonly_fields = ('show_update_url', 'show_delete_url',)
    def show_delete_url(self, obj):
        if not obj.uuid:
            return ''
        return format_html("<a target='_blank' onclick='return confirm(\"Are you sure?\")' href='{url}'>{uuid}</a>", url=reverse('communities:delete', args=[obj.uuid]), uuid=obj.uuid)
    def show_update_url(self, obj):
        if not obj.uuid:
            return ''
        return format_html("<a target='_blank' href='{url}'>{uuid}</a>", url=reverse('communities:update', args=[obj.uuid]), uuid=obj.uuid)

    show_delete_url.short_description = "Delete URL"
    show_update_url.short_description = "Update URL"

admin.site.register(Community, CommunityAdmin)
admin.site.register(Style)
admin.site.register(Contact)
admin.site.register(EventCounter)
admin.site.register(UpdateRequest, UpdateRequestAdmin)
