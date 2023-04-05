from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.utils import json
from evaluation.models.bpmn_file import BPMNFile
from evaluation.models.evaluated_result import EvaluatedResult
from evaluation.models.project import Project
from evaluation.models.user import User
from usecase.evaluate.evaluate import Evaluate
from django.core.files.storage import FileSystemStorage


class BPEResponse:
    err: str
    data: object

    def __init__(self, err, data) -> None:
        self.err = err
        self.data = data


def load_request_body(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body
