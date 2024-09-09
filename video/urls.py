from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.get_video),
    path('', views.index),
]
