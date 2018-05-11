from django.urls import path

from . import views

urlpatterns = [
    path('healthcheck', views.get_health, name='health'),
    path('dataset/samples', views.get_dataset_samples, name='dataset_samples'),
    path(
        'dataset/scribbles/<str:sequence>/<int:scribble_idx>',
        views.get_scribble,
        name='dataset_scribbles'),
    path('evaluation/interaction', views.post_predicted_masks, name='evaluate'),
    path('evaluation/report', views.get_report, name='report'),
    path('evaluation/finish', views.post_finish, name='finish'),
]
