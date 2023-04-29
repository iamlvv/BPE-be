from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.evaluated_result import EvaluatedResultView

urlpatterns_result = [
    path('result/<int:project_id>/save', EvaluatedResultView.save),
    path('result/all', EvaluatedResultView.get_result_by_bpmn_file),
    path('result', EvaluatedResultView.get),
    path('result/delete', EvaluatedResultView.delete)
]

urlpatterns_result = format_suffix_patterns(urlpatterns_result)
