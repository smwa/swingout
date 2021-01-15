from django.urls import path

from . import views

app_name = 'communities'
urlpatterns = [
    path('', views.index, name='index'),
    path('requests/', views.requestUpdate, name='requestUpdate'),
]
