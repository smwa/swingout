from django.urls import path

from . import views

app_name = 'public'
urlpatterns = [
    path('', views.map, name='map'),
    path('index.html', views.map, name='map'),
    path('addCommunity.html', views.addCommunity, name='addCommunity'),
]
