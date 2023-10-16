from .utils import *
import jsonpickle


@bpsky.route("/api/v1/workspace", methods=["POST"])
def createNewWorkspace():
    try:
        body = load_request_body(request)
        user_id = get_id_from_token(get_token(request))
        if "name" not in body:
            raise Exception("name required")
        name = body["name"]
        description = body["description"] if "description" in body else ""
        createdAt = datetime.now()
        background = body["background"] if "background" in body else ""
        icon = body["icon"] if "icon" in body else ""
        isPersonal = body["isPersonal"] if "isPersonal" in body else False
        isDeleted = body["isDeleted"] if "isDeleted" in body else False
        data = WorkspaceUseCase.createNewWorkspace(
            name=name,
            description=description,
            createdAt=createdAt,
            ownerId=user_id,
            background=background,
            icon=icon,
            isPersonal=isPersonal,
            isDeleted=isDeleted,
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/<string:workspaceId>", methods=["GET", "DELETE"])
def workspace_workspace(workspaceId):
    try:
        if request.method == "DELETE":
            return getWorkspace(workspaceId)
        else:
            return deleteWorkspace(workspaceId)
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


def getWorkspace(workspaceId):
    user_id = get_id_from_token(get_token(request))
    result = WorkspaceUseCase.getWorkspace(workspaceId)
    return bpsky.response_class(
        response=json.dumps(result, default=json_serial),
        status=200,
        mimetype="application/json",
    )


def deleteWorkspace(workspaceId):
    user_id = get_id_from_token(get_token(request))
    WorkspaceUseCase.deleteWorkspace(workspaceId)
    return "Delete successfully"
