import json
from datetime import date, datetime
from auth.jwt import *
from bpsky import bpsky
from flask import request, redirect
from usecase.evaluate.evaluate import Evaluate
from usecase.evaluate.compare import Compare
from usecase.project import ProjectUsecase
from usecase.user import UserUsecase
from usecase.process_version import ProcessVersionUsecase
from usecase.process import ProcessUsecase
from usecase.evaluate_result import EvaluatedResultUsercase
from usecase.image import ImageUsecase
from usecase.workspace import WorkspaceUseCase
from usecase.join_workspace import JoinWorkspaceUseCase
from usecase.request import RequestUseCase
from bpsky import socketio


def load_request_body(request):
    try:
        body = request.get_json()
    except Exception as e:
        raise Exception("body required")
    return body


def get_token(request):
    if "Authorization" in request.headers:
        return request.headers["Authorization"].split()[1]

    raise Exception("invalid token")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_xml_link(project_id, process_id, version):
    return f"static/{project_id}/{process_id}/{version}.bpmn"
