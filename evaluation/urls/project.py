from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.project import ProjectView

urlpatterns_project = [
    path('project', ProjectView.insert),
    path('project/<int:project_id>', ProjectView.get_project),
    # path('project/<int:project_id>/document', ProjectView.get_description),
    path('project/<int:project_id>/document/update', ProjectView.update_document),
    path('project/<int:project_id>/user', ProjectView.get_all_user),
    path('project/<int:project_id>/user/grant', ProjectView.grant_user),
    path('project/<int:project_id>/user/update', ProjectView.update_all_user),
    path('project/<int:project_id>/user/revoke', ProjectView.revoke_user),
    path('project/all', ProjectView.get_all_project_by_user_id),
]

urlpatterns_project = format_suffix_patterns(urlpatterns_project)
