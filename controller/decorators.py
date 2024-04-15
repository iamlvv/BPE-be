from functools import wraps

import jsonpickle
from flask import request

from controller.utils import get_id_from_token, get_token, load_request_body
from services.utils import Permission_check


def permission_project_check(func):
    @wraps(func)
    def decorator_function(*args, **kwargs):
        user_id = get_id_from_token(get_token(request))
        if request.method == "GET":
            project_id = request.args.get("projectId")
        else:
            body = load_request_body(request)
            project_id = body["projectId"]
        if not Permission_check.check_user_has_access_survey(project_id, user_id):
            # return bpsky.response_class(
            #     response=jsonpickle.encode(
            #         {"message": "User does not have access to this survey"},
            #         unpicklable=False,
            #     ),
            #     status=403,
            #     mimetype="application/json",
            # )
            raise Exception("User does not have access to this survey")
        return func(*args, **kwargs)

    return decorator_function


def permission_workspace_check(func):
    @wraps(func)
    def decorator_function(*args, **kwargs):
        user_id = get_id_from_token(get_token(request))
        if request.method == "GET":
            workspace_id = request.args.get("workspaceId")
        else:
            body = load_request_body(request)
            workspace_id = body["workspaceId"]
        check = Permission_check.check_if_user_is_workspace_owner(workspace_id, user_id)
        if check is False:
            # return bpsky.response_class(
            #     response=jsonpickle.encode(
            #         {"message": "User does not have access to this workspace"},
            #         unpicklable=False,
            #     ),
            #     status=403,
            #     mimetype="application/json",
            # )
            raise Exception("User does not have access to this workspace")
        elif check == "Workspace not found":
            raise Exception("Workspace not found")
        return func(*args, **kwargs)

    return decorator_function
