from django.urls import path

from . import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('success/', views.success, name='registration_success')
]
