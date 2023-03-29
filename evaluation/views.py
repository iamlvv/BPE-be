from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from evaluation.models import *

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
    @api_view(['GET', 'POST'])
    def insert(request, format=None):
        if request.method == "POST":
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
        Project.insert(body["document_link"], body["name"])
        return Response("Insert successfully")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        return Project.get_all()


class BPMNFileView:
    @staticmethod
    @api_view(["POST"])
    def save(request):
        body = load_request_body(request)
        BPMNFile.insert(body["xml_file_link"], body["project_id"], body["version"])
        # TODO: Saving result of evaluation when saving bpmn file
        json_response = [r.__dict__ for r in Evaluate.evaluate(body["json_payload"])]
        EvaluatedResult.save(json_response)
        return Response("Save successfully")

    @staticmethod
    @api_view(["GET"])
    def get_file_by_project(request, project_id):
        return Response(project_id)


class EvaluatedResultView:
    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        data = list(EvaluatedResult.objects.values())
        return JsonResponse(data, safe=False)

    @staticmethod
    @api_view(["GET"])
    def get_evaluation_result_by_file(request):
        pass
