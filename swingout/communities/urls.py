from django.urls import path

from . import views

app_name = 'communities'
urlpatterns = [
    path('index.html', views.map, name='map'),
    path('', views.map, name='map'),
    path('api/communities', views.index, name='index'),
    path('communities/add', views.add, name='add'), # Only used for reverse url lookups
    path('communities/add/<latitude>/<longitude>', views.add, name='addWithCoordinates'),
    path('communities/add/preview', views.add_preview, name='addPreview'),
    path('communities/delete/<uuid:uuid>', views.delete, name='delete'),
    path('communities/update/<uuid:uuid>', views.update, name='update'),
    path('communities/thankYou/<uuid:uuid>', views.thankYou, name='thankYou'),
    path('communities/requestUpdate', views.requestUpdate, name='requestUpdate'), # Only used for reverse url lookups
    path('communities/requestUpdate/<uuid:uuid>', views.requestUpdate, name='requestUpdateWithUuid'),
    path('api/communities/requestUpdate/delete/<uuid:uuid>', views.markUpdateRequestHandled, name='markUpdateRequestHandled'),
    path('manifest.json', views.manifest, name='manifest'),
    path('service-worker.js', views.serviceWorker, name='serviceWorker'),
]
