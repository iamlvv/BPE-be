from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.project import ProjectView

urlpatterns_project = [
    path('project', ProjectView.insert),
    path('project/all', ProjectView.get_all),
]

urlpatterns_project = format_suffix_patterns(urlpatterns_project)
