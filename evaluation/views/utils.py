from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.utils import json
from evaluation.usecase.evaluate.evaluate import Evaluate
from evaluation.usecase.evaluate.compare import Compare
from evaluation.usecase.project import ProjectUsecase
from evaluation.usecase.user import UserUsecase
from evaluation.usecase.bpmn_file import BPMNFileUsecase
from evaluation.usecase.evaluate_result import EvaluatedResultUsercase
from evaluation.usecase.image import ImageUsecase
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict
from evaluation.auth.jwt import *


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


def get_token(request):
    if "Authorization" in request.headers:
        return request.headers["Authorization"].split()[1]

    raise Exception("invalid token")
