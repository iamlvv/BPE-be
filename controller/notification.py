from .utils import *
import jsonpickle


@bpsky.route("/api/v1/user/notification", methods=["GET"])
def getAllNotifications():
    try:
        userId = get_id_from_token(get_token(request))
        keyword = request.args.get("keyword", None)
        page = request.args.get("page", 0)
        limit = request.args.get("limit", 10)
        isStarred = request.args.get("isStarred", False)
        data = NotificationUseCase.getAllNotifications(
            userId, page, limit, isStarred, keyword
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/notification", methods=["POST"])
def insertNewNotification():
    try:
        body = load_request_body(request)
        userId = body["userId"]
        content = body["content"]
        createdAt = datetime.now()
        isDeleted = False
        isStarred = False
        isRead = False
        data = NotificationUseCase.insertNewNotification(
            userId=userId,
            content=content,
            createdAt=createdAt,
            isDeleted=isDeleted,
            isStarred=isStarred,
            isRead=isRead,
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/notification/deletion", methods=["POST"])
def deleteNotification():
    try:
        body = load_request_body(request)
        notificationIdList = body["notificationIdList"]
        deletedAt = datetime.now()
        data = NotificationUseCase.deleteNotification(notificationIdList, deletedAt)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/notification/star", methods=["POST"])
def starNotification():
    try:
        body = load_request_body(request)
        notificationId = body["notificationId"]
        data = NotificationUseCase.starNotification(notificationId)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/notification/read", methods=["POST"])
def readNotification():
    try:
        body = load_request_body(request)
        notificationId = body["notificationId"]
        data = NotificationUseCase.readNotification(notificationId)
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)
