from models.request import Request


class RequestUseCase:
    @classmethod
    def getAllRequests(cls, workspaceId, keyword=None, type=None, status=None):
        requestsList = Request.getAllRequests(workspaceId, keyword, type, status)
        return requestsList

    @classmethod
    def insertNewRequest(
        cls,
        requestType,
        content,
        createdAt,
        status,
        workspaceId,
        senderId,
        recipientId,
        handlerId,
        fr_permission="",
        to_permission="",
        rcp_permission="",
    ):
        newRequest = Request.insertNewRequest(
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
        return newRequest

    @classmethod
    def deleteRequests(cls, workspaceId, requestIdList, deletedAt):
        deletedRequests = Request.deleteRequests(workspaceId, requestIdList, deletedAt)
        return deletedRequests

    @classmethod
    def approveRequest(cls, id):
        request = Request.approveRequest(id)
        return request

    @classmethod
    def declineRequest(cls, id):
        request = Request.declineRequest(id)
        return request
