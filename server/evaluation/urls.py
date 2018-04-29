from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('dataset/samples', views.get_dataset_samples, name='dataset_samples'),
    path(
        'dataset/scribbles/<str:sequence>/<int:scribble_idx>',
        views.get_scibble,
        name='dataset_scribbles'),
    path('evaluation/interaction', views.post_predicted_masks, name='evaluate'),
    path('evaluation/report', views.get_report, name='report'),
]  # + static(
# 'dataset/scribbles',
# document_root=
# '/Users/alberto/Workspace/CVL/datasets/davis-2017/data/DAVIS/Scribbles')
