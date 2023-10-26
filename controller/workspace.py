from .utils import *
import jsonpickle
import cloudinary
import cloudinary.uploader


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
        deletedAt = datetime.now()
        data = WorkspaceUseCase.deleteWorkspace(workspaceId, deletedAt)
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


@bpsky.route("/api/v1/workspace/backgrounduploading", methods=["POST"])
# using form-data to upload file
# def allowed_file(filename: str):
#     ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# def secure_filename(filename: str):
#     return filename.replace(" ", "_")


# upload file using form-data and save to cloudinary
def uploadBackground():
    try:
        user_id = get_id_from_token(get_token(request))
        workspaceId = request.form["workspaceId"]
        # check if user is owner of workspace
        checkResult = checkWorkspaceOwner(workspaceId, user_id)
        if checkResult is not True:
            raise Exception(checkResult)
        # upload background
        if "background" not in request.files:
            raise Exception("No file part")
        file = request.files["background"]
        print(file)
        if file.filename == "":
            raise Exception("No selected file")
        if file:
            cloudinary.config(
                cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
                api_key=os.environ.get("CLOUDINARY_API_KEY"),
                api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
                secure=True,
            )
            upload_result = cloudinary.uploader.upload(file)
            data = WorkspaceUseCase.updateWorkspaceBackground(
                workspaceId, upload_result["secure_url"]
            )
            return "Upload background success"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/iconuploading", methods=["POST"])
# upload file using form-data and save to cloudinary
def uploadIcon():
    try:
        user_id = get_id_from_token(get_token(request))
        workspaceId = request.form["workspaceId"]
        # check if user is owner of workspace
        checkResult = checkWorkspaceOwner(workspaceId, user_id)
        if checkResult is not True:
            raise Exception(checkResult)
        # upload icon
        if "icon" not in request.files:
            raise Exception("No file part")
        file = request.files["icon"]
        print(file)
        if file.filename == "":
            raise Exception("No selected file")
        if file:
            cloudinary.config(
                cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
                api_key=os.environ.get("CLOUDINARY_API_KEY"),
                api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
                secure=True,
            )
            upload_result = cloudinary.uploader.upload(file)
            data = WorkspaceUseCase.updateWorkspaceIcon(
                workspaceId, upload_result["secure_url"]
            )
            return "Upload icon success"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/me/all", methods=["GET"])
# get all workspaces that user is member of or owner of
# user can filter by openedAt by passing openedAt in query params, default is None. Latest to oldest, and vice versa.
# user can filter by ownerId by passing ownerId in query params, default is None
# user can search by keyword by passing keyword in query params, default is None
# pagination for this endpoint too. default is 0, 10
def getAllWorkspaces():
    try:
        user_id = get_id_from_token(get_token(request))
        openedAt = request.args.get("openedAt", None)
        ownerId = request.args.get("ownerId", None)
        keyword = request.args.get("keyword", None)
        page = request.args.get("page", 0)  # default is 0
        limit = request.args.get("limit", 10)  # default is 10
        pinned = request.args.get("pinned", None)
        print(openedAt, ownerId, keyword, page, limit)
        data = WorkspaceUseCase.getAllWorkspacesByUser(
            user_id, page, limit, openedAt, ownerId, keyword, pinned
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/pinned", methods=["POST"])
def pinWorkspace():
    try:
        body = load_request_body(request)
        userId = get_id_from_token(get_token(request))
        workspaceId = body["workspaceId"]
        data = WorkspaceUseCase.pinWorkspace(userId, workspaceId)
        return data
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/me/pinned", methods=["GET"])
def getPinnedWorkspace():
    try:
        user_id = get_id_from_token(get_token(request))
        data = WorkspaceUseCase.getPinnedWorkspace(user_id)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/search/<string:keyword>", methods=["GET"])
# search workspace by keyword, search in name and description
def searchWorkspaceByKeyword(keyword):
    try:
        userId = get_id_from_token(get_token(request))
        data = WorkspaceUseCase.searchWorkspaceByKeyword(keyword, userId)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/open", methods=["POST"])
# open workspace and add to recent opened workspace
def openWorkspace():
    try:
        body = load_request_body(request)
        workspaceId = body["workspaceId"]
        userId = get_id_from_token(get_token(request))
        openedAt = datetime.now()
        data = WorkspaceUseCase.openWorkspace(userId, workspaceId, openedAt)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)
