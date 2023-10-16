from .utils import *


@bpsky.route("/api/v1/project", methods=["POST"])
def project_insert():
    try:
        body = load_request_body(request)
        user_id = get_id_from_token(get_token(request))
        if "name" not in body:
            raise Exception("name required")
        name = body["name"]
        description = body["description"] if "description" in body else ""
        data = ProjectUsecase.create(description, name, user_id)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/project/<int:project_id>", methods=["GET", "DELETE"])
def project_project(project_id):
    try:
        if request.method == "GET":
            return project_get_project(project_id)
        else:
            return project_delete_project(project_id)
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


def project_get_project(project_id):
    user_id = get_id_from_token(get_token(request))
    result = ProjectUsecase.get(project_id, user_id)
    return bpsky.response_class(
        response=json.dumps(result, default=json_serial),
        status=200,
        mimetype="application/json",
    )


def project_delete_project(project_id):
    user_id = get_id_from_token(get_token(request))
    ProjectUsecase.delete(project_id, user_id)
    return "Delete successfully"


@bpsky.route("/api/v1/project/all", methods=["GET"])
def project_get_all_project_by_user_id():
    try:
        user_id = get_id_from_token(get_token(request))
        result = ProjectUsecase.get_all_project_by_user_id(user_id)
        return bpsky.response_class(
            response=json.dumps(result, default=json_serial),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/project/all/owned", methods=["GET"])
def project_get_all_owned_project_by_user_id():
    try:
        user_id = get_id_from_token(get_token(request))
        result = ProjectUsecase.get_all_owned_project_by_user_id(user_id)
        return bpsky.response_class(
            response=json.dumps(result, default=json_serial),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/project/all/shared", methods=["GET"])
def project_get_all_shared_project_by_user_id():
    try:
        user_id = get_id_from_token(get_token(request))
        result = ProjectUsecase.get_all_shared_project_by_user_id(user_id)
        return bpsky.response_class(
            response=json.dumps(result, default=json_serial),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


# @bpsky.route("/api/v1/")
# def project_get_all(request):
#     return JsonResponse(ProjectUsecase.get_all(), status=status.HTTP_200_OK, safe=False)


@bpsky.route("/api/v1/project/<int:project_id>/name", methods=["PUT"])
def project_update_name(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        if "name" not in body:
            raise Exception("name required")
        name = body["name"]
        ProjectUsecase.update_name(user_id, project_id, name)
        return "Update successfully"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/project/<int:project_id>/description", methods=["PUT"])
def project_update_description(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        if "description" not in body:
            raise Exception("description required")
        description = body["description"]
        ProjectUsecase.update_description(user_id, project_id, description)
        return "Update successfully"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/project/<int:project_id>/document", methods=["GET"])
def project_get_document(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        data = ProjectUsecase.get_document(user_id, project_id)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/project/<int:project_id>/document/text", methods=["GET", "PUT"])
def project_document_content(project_id):
    try:
        if request.method == "GET":
            return project_get_document_content(project_id)
        else:
            return project_update_document(project_id)
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


def project_get_document_content(project_id):
    user_id = get_id_from_token(get_token(request))
    msg = ProjectUsecase.get_document_content(user_id, project_id)
    return msg


def project_update_document(project_id):
    user_id = get_id_from_token(get_token(request))
    if "file" not in request.files:
        raise Exception("file required")
    file = request.files["file"]
    document_link = f"static/{project_id}/readme.md"
    return ProjectUsecase.update_document(user_id, project_id, document_link, file)


@bpsky.route(
    "/api/v1/project/<int:project_id>/user", methods=["GET", "PUT", "POST", "DELETE"]
)
def project_permission_user(project_id):
    try:
        if request.method == "GET":
            return project_get_all_user(project_id)
        if request.method == "PUT":
            return project_update_all_user(project_id)
        elif request.method == "POST":
            return project_grant_user(project_id)
        else:
            return project_revoke_user(project_id)
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


def project_get_all_user(project_id):
    user_id = get_id_from_token(get_token(request))
    data = ProjectUsecase.get_all_user_by_project_id(user_id, project_id)
    return bpsky.response_class(
        response=json.dumps(data, default=json_serial),
        status=200,
        mimetype="application/json",
    )


def project_update_all_user(project_id):
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    return ProjectUsecase.update_permission(user_id, project_id, body)


def project_revoke_user(project_id):
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    if type(body) is not list:
        return bpsky.response_class(response="bad request", status=400)
    return ProjectUsecase.revoke_permission(user_id, body, project_id)


def project_grant_user(project_id):
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    return ProjectUsecase.grant_permission(user_id, project_id, body)
