from django.urls import path

from . import views

app_name = 'communities'
urlpatterns = [
    path('index.html', views.map, name='map'),
    path('', views.map, name='map'),
    path('manifest.json', views.manifest, name='manifest'),
    path('api/communities', views.index, name='index'),
    path('communities/add', views.add, name='add'), # Only used for reverse url lookups
    path('communities/add/<latitude>/<longitude>', views.add, name='addWithCoordinates'),
    path('communities/thankYou', views.thankYou, name='thankYou'),
    path('communities/requestUpdate', views.requestUpdate, name='requestUpdate'), # Only used for reverse url lookups
    path('communities/requestUpdate/<uuid:uuid>', views.requestUpdate, name='requestUpdateWithUuid'),
]
