from django.urls import path

from . import views

app_name = 'public'
urlpatterns = [
    path('index.html', views.map, name='map'),
    path('', views.map, name='map'),
]
