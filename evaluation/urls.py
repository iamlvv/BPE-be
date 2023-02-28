from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation import views

urlpatterns = [
    path('test/', views.test_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
