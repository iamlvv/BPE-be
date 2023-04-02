from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation import views

urlpatterns = [
    path('evaluate', views.EvaluateView.evaluate),
    path('user', views.UserView.insert),
    path('user/all', views.UserView.get_all),
    path('project', views.ProjectView.insert),
    path('project/all', views.ProjectView.get_all),
    path('bpmnFile/save', views.BPMNFileView.save),
    path('bpmnFile/version/<str:version>', views.BPMNFileView.get_by_version),
    path('bpmnFile/project/<int:project_id>', views.BPMNFileView.get_by_project),

    path('result/save', views.EvaluatedResultView.save),
    path('result/all', views.EvaluatedResultView.get_all)
]

urlpatterns = format_suffix_patterns(urlpatterns)
