import os

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from evaluation.models import *
import shutil

from usecase.evaluate.evaluate import Evaluate


def load_request_body(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body


class EvaluateView:
    @staticmethod
    @api_view(['POST'])
    def evaluate(request, format=None):
        body = load_request_body(request)
        result = Evaluate.evaluate(body)
        json_response = [r.__dict__ for r in result]
        return JsonResponse(json_response, safe=False)


class UserView:
    @staticmethod
    @api_view(['POST'])
    def insert(request, format=None):
        body = load_request_body(request)
        password = body["password"]
        name = body["name"]
        email = body["email"]
        phone = body["phone"]
        avatar = body["avatar"]
        user = User.create(password, email, name, phone, avatar)
        user.save()
        return Response("Insert successfully")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        data = list(User.objects.values())
        return JsonResponse(data, safe=False)


class ProjectView:
    @staticmethod
    @api_view(['POST'])
    def insert(request):
        body = load_request_body(request)
        Project.insert(body["document"], body["name"], body["user_id"])
        return Response("Insert successfully")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        return Project.get_all()


class BPMNFileView:
    @staticmethod
    @api_view(["POST"])
    def save(request):
        file = request.FILES['file']
        project_id = request.POST['project_id']

        fs = FileSystemStorage()

        filename = fs.save('static/' + file.name, file)
        uploaded_file_url = fs.url(filename)

        BPMNFile.insert(uploaded_file_url, project_id)
        return Response("Save successfully")

    @staticmethod
    @api_view(["GET"])
    def get_by_project(request, project_id):
        return BPMNFile.get_by_project(project_id)

    @staticmethod
    @api_view(["GET"])
    def get_by_version(request, version):
        return BPMNFile.get_by_version(version)


class EvaluatedResultView:
    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        data = list(EvaluatedResult.objects.values())
        return JsonResponse(data, safe=False)

    @staticmethod
    @api_view(['POST'])
    def save(request):
        body = load_request_body(request)
        EvaluatedResult.insert(
            body["xmlFileLink"],
            body['projectID'],
            body['result'],
        )
        return Response("Save successfully")


@staticmethod
@api_view(["GET"])
def get_evaluation_result_by_file(request):
    pass
