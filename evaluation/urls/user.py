from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.user import UserView

urlpatterns_user = [
    path('user', UserView.insert),
    path('user/all', UserView.get_all),
]

urlpatterns_user = format_suffix_patterns(urlpatterns_user)
