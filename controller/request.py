from .utils import *
import jsonpickle


@bpsky.route("/api/v1/request", methods=["GET"])
def getAllRequests():
    try:
        workspaceId = request.args.get("workspaceId")
        keyword = request.args.get("keyword", None)
        type = request.args.get("type", None)
        status = request.args.get("status", None)
        page = request.args.get("page", 0)
        limit = request.args.get("limit", 10)
        data = RequestUseCase.getAllRequests(
            workspaceId, page, limit, keyword, type, status
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/request", methods=["POST"])
def insertNewRequest():
    try:
        body = load_request_body(request)
        handlerId = get_id_from_token(get_token(request))
        requestType = body["requestType"]
        content = body["content"]
        createdAt = datetime.now()
        status = "pending"
        workspaceId = body["workspaceId"]
        senderId = body["senderId"]
        recipientId = body["recipientId"]
        fr_permission = body["fr_permission"] if "fr_permission" in body else ""
        to_permission = body["to_permission"] if "to_permission" in body else ""
        rcp_permission = body["rcp_permission"] if "rcp_permission" in body else ""
        if fr_permission == "" and to_permission == "" and rcp_permission == "":
            raise Exception("No permission is set")

        newRequest = RequestUseCase.insertNewRequest(
            requestType,
            content,
            createdAt,
            status,
            workspaceId,
            senderId,
            recipientId,
            handlerId,
            fr_permission,
            to_permission,
            rcp_permission,
        )
        return bpsky.response_class(
            response=jsonpickle.encode(newRequest, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/request/deletion", methods=["POST"])
def deleteRequest():
    try:
        body = load_request_body(request)
        deletedRequests = RequestUseCase.deleteRequests(
            body["workspaceId"], body["requestIdList"], body["deletedAt"]
        )
        return bpsky.response_class(
            response=jsonpickle.encode(deletedRequests, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/request/approve", methods=["POST"])
def approveRequest():
    try:
        body = load_request_body(request)
        handlerId = get_id_from_token(get_token(request))
        requestIdList = body["requestIdList"]
        workspaceId = body["workspaceId"]
        data = RequestUseCase.approveRequest(workspaceId, requestIdList, handlerId)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)


@bpsky.route("/api/v1/request/decline", methods=["POST"])
def declineRequest():
    try:
        body = load_request_body(request)
        handlerId = get_id_from_token(get_token(request))
        requestIdList = body["requestIdList"]
        workspaceId = body["workspaceId"]
        data = RequestUseCase.declineRequest(workspaceId, requestIdList, handlerId)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        raise Exception(e)
