from .utils import *
import jsonpickle


# check if user is owner of workspace
def checkWorkspaceOwner(workspaceId: str, ownerId: str):
    check = WorkspaceUseCase.checkWorkspaceOwner(workspaceId, ownerId)
    if check is None:
        raise Exception("Workspace not found")
    if check is False:
        raise Exception("You are not owner of this workspace")
    return True


# create new workspace
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


@bpsky.route("/api/v1/workspace/<workspaceId>", methods=["GET"])
def getWorkspace(workspaceId):
    try:
        result = WorkspaceUseCase.getWorkspace(workspaceId)
        if result is None:
            raise Exception("Workspace not found")
        else:
            return bpsky.response_class(
                response=jsonpickle.encode(result, unpicklable=False),
                status=200,
                mimetype="application/json",
            )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


# delete workspace
@bpsky.route("/api/v1/workspace/deletion", methods=["POST"])
def deleteWorkspace():
    try:
        body = load_request_body(request)
        user_id = get_id_from_token(get_token(request))
        workspaceId = body["workspaceId"]
        # check if user is owner of workspace
        checkResult = checkWorkspaceOwner(workspaceId, user_id)
        if checkResult is not True:
            raise Exception(checkResult)
        # delete workspace
        data = WorkspaceUseCase.deleteWorkspace(workspaceId)
        return "Delete Workspace Success"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


# update name and description
@bpsky.route("/api/v1/workspace/nameupdation", methods=["POST"])
def updateWorkspaceName():
    try:
        body = load_request_body(request)
        user_id = get_id_from_token(get_token(request))
        workspaceId = body["workspaceId"]
        name = body["name"]
        # check if user is owner of workspace
        checkResult = checkWorkspaceOwner(workspaceId, user_id)
        if checkResult is not True:
            raise Exception(checkResult)
        # update name
        data = WorkspaceUseCase.updateWorkspaceName(workspaceId, name)
        return "Update name success"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/descriptionupdation", methods=["POST"])
def updateWorkspaceDescription():
    try:
        body = load_request_body(request)
        user_id = get_id_from_token(get_token(request))
        workspaceId = body["workspaceId"]
        description = body["description"]
        # check if user is owner of workspace
        checkResult = checkWorkspaceOwner(workspaceId, user_id)
        if checkResult is not True:
            raise Exception(checkResult)
        # update description
        data = WorkspaceUseCase.updateWorkspaceDescription(workspaceId, description)
        return "Update description success"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/ownerchange", methods=["POST"])
def changeOwner():
    try:
        body = load_request_body(request)
        user_id = get_id_from_token(get_token(request))
        workspaceId = body["workspaceId"]
        newOwnerId = body["newOwnerId"]
        # check if user is owner of workspace
        checkResult = checkWorkspaceOwner(workspaceId, user_id)
        if checkResult is not True:
            raise Exception(checkResult)
        # update owner
        data = WorkspaceUseCase.changeOwnership(workspaceId, newOwnerId)
        return "Change owner success"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)
