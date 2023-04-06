from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.evaluate import EvaluateView

urlpatterns_evaluate = [
    path('evaluate', EvaluateView.evaluate),
    path('evaluate/compare', EvaluateView.compare),
]

urlpatterns_evaluate = format_suffix_patterns(urlpatterns_evaluate)
