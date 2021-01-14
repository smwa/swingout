from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('requests/', views.requestUpdate, name='requestUpdate'),
]
