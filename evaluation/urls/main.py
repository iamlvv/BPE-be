from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def check(request):
    return HttpResponse("Business process evaluation")


urlpatterns_main = [
    path('', check),
]

urlpatterns_main = format_suffix_patterns(urlpatterns_main)
