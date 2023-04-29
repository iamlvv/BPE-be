from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.bpmn_file import BPMNFileView

urlpatterns_bpmn_file = [
    path('bpmnfile/<int:project_id>', BPMNFileView.get_by_project),
    path('bpmnfile/<int:project_id>/create', BPMNFileView.create_new_version),
    path('bpmnfile/<int:project_id>/<str:version>/save', BPMNFileView.save),
    path('bpmnfile/<int:project_id>/<str:version>',
         BPMNFileView.get_by_version),
    path('bpmnfile/<int:project_id>/<str:version>/delete',
         BPMNFileView.delete_version),
    path('bpmnfile/<int:project_id>/<str:version>/delete_oldest',
         BPMNFileView.delete_oldest_version),
    path('bpmnfile/comment', BPMNFileView.get_comment_by_bpmn_file),
    path('bpmnfile/comment/add', BPMNFileView.comment),
    path('bpmnfile/comment/edit', BPMNFileView.edit_comment),
    path('bpmnfile/comment/delete', BPMNFileView.delete_comment),
    path('bpmnfile/comment/user', BPMNFileView.get_comment_by_user),
]

urlpatterns_bpmn_file = format_suffix_patterns(urlpatterns_bpmn_file)
