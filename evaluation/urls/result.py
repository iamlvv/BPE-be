from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.evaluated_result import EvaluatedResultView

urlpatterns_result = [
    path('result/save', EvaluatedResultView.save),
    path('result/all', EvaluatedResultView.get_all)
]

urlpatterns_result = format_suffix_patterns(urlpatterns_result)
