from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from evaluation.views.user import UserView

urlpatterns_user = [
    path('user', UserView.get),
    path('user/verify/<str:token>', UserView.verify),
    path('user/signup', UserView.signup),
    path('user/all', UserView.get_all),
    path('user/signin', UserView.signin),
]

urlpatterns_user = format_suffix_patterns(urlpatterns_user)
