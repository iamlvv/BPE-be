from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.user import UserView

urlpatterns_oauth2 = [
    path('auth/login/google', UserView.auth_with_google),
    path('auth/login/google/callback', UserView.callback),
]

urlpatterns_oauth2 = format_suffix_patterns(urlpatterns_oauth2)
