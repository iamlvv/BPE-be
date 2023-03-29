from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation import views

urlpatterns = [
    path('evaluate/', views.EvaluateView.evaluate),
    path('user/', views.UserView.insert),
    path('user/all', views.UserView.get_all),
    path('project/', views.ProjectView.insert),
    path('project/all', views.ProjectView.get_all),
    path('file/<int:project_id>', views.BPMNFileView.get_file_by_project)
]

urlpatterns = format_suffix_patterns(urlpatterns)
