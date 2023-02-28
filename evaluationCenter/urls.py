
from django.urls import path, include

urlpatterns = [
    path("evaluate/", include("evaluation.urls")),
]
