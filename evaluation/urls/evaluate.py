from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.evaluate import EvaluateView

urlpatterns_evaluate = [
    path('evaluate', EvaluateView.evaluate),
    path('evaluate/compare', EvaluateView.compare),
    path('evaluate/selling_as_is', EvaluateView.evaluate1),
    path('evaluate/selling_to_be', EvaluateView.evaluate2),
    path('evaluate/rescheduling_as_is', EvaluateView.evaluate3),
    path('evaluate/rescheduling_to_be', EvaluateView.evaluate4),
]

urlpatterns_evaluate = format_suffix_patterns(urlpatterns_evaluate)
