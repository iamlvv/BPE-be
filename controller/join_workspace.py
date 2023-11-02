from .utils import *
import jsonpickle


@bpsky.route("/api/v1/workspace/members", methods=["GET"])
def getAllMembers():
    try:
        print("masuk")
        keyword = request.args.get("keyword", None)
        page = request.args.get("page", 0)
        limit = request.args.get("limit", 10)
        permission = request.args.get("permission", None)
        body = load_request_body(request)
        workspaceId = body["workspaceId"]
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
