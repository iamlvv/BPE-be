from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.bpmn_file import BPMNFileView

urlpatterns_bpmn_file = [
    path('bpmnFile/save', BPMNFileView.save),
    path('bpmnFile/version/<str:version>', BPMNFileView.get_by_version),
    path('bpmnFile/project/<int:project_id>', BPMNFileView.get_by_project),
]

urlpatterns_bpmn_file = format_suffix_patterns(urlpatterns_bpmn_file)
