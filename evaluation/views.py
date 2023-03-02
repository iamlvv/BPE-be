from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json

from usecase.evaluate.evaluate import Evaluate


@api_view(['GET', 'POST'])
def test_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        return Response(Evaluate.a)

    elif request.method == 'POST':
        e = Evaluate()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        e.evaluate(body)
        json_response = e.result.__dict__
        return Response(json_response)

    elif request.method == "PUT":
        return Response("Test put")
