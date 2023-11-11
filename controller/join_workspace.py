from .utils import *
import jsonpickle


@bpsky.route("/api/v1/workspace/<string:workspaceId>/members", methods=["GET"])
def getAllMembers(workspaceId):
    try:
        keyword = request.args.get("keyword", None)
        page = request.args.get("page", 0)
        limit = request.args.get("limit", 10)
        permission = request.args.get("permission", None)
        # body = load_request_body(request)
        # workspaceId = body["workspaceId"]
        data = JoinWorkspaceUseCase.getAllMembers(
            workspaceId, page, limit, keyword, permission
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/workspace/members", methods=["POST"])
def insertNewMember():
    try:
        body = load_request_body(request)
        memberId = body["memberId"]
        workspaceId = body["workspaceId"]
        joinedAt = datetime.now()
        permission = body["permission"]
        data = JoinWorkspaceUseCase.insertNewMember(
            memberId, workspaceId, joinedAt, permission
        )
        if data is None:
            return bpsky.response_class(
                response=jsonpickle.encode(
                    {"message": "Member already joined workspace"},
                    unpicklable=False,
                ),
                status=400,
                mimetype="application/json",
            )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route(
    "/api/v1/workspace/<string:workspaceId>/members/permission", methods=["GET"]
)
def getPermissionOfUser(workspaceId):
    try:
        body = load_request_body(request)
        memberId = get_id_from_token(get_token(request))
        data = JoinWorkspaceUseCase.getPermissionOfUser(memberId, workspaceId)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/workspace/members/permission", methods=["POST"])
def updatePermission():
    try:
        body = load_request_body(request)
        workspaceId = body["workspaceId"]
        memberIdList = body["memberIdList"]
        permission = body["permission"]
        data = JoinWorkspaceUseCase.updateMemberPermission(
            workspaceId, memberIdList, permission
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/workspace/members/deletion", methods=["POST"])
def deleteMember():
    try:
        body = load_request_body(request)
        workspaceId = body["workspaceId"]
        memberIdList = body["memberIdList"]
        leftAt = datetime.now()
        data = JoinWorkspaceUseCase.deleteMember(workspaceId, memberIdList, leftAt)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/workspace/members/undodeletion", methods=["POST"])
def undoDeleteMember():
    try:
        body = load_request_body(request)
        workspaceId = body["workspaceId"]
        memberIdList = body["memberIdList"]
        data = JoinWorkspaceUseCase.undoDeleteMember(workspaceId, memberIdList)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)
