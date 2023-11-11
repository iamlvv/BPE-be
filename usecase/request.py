from models.request import Request


class RequestUseCase:
    @classmethod
    def getAllRequests(cls, workspaceId):
        requestsList = Request.getAllRequests(workspaceId)
        return requestsList

    def insertNewRequest(
        cls,
        type,
        content,
        createdAt,
        status,
        isDeleted,
        isWorkspaceDeleted,
        workspaceId,
        senderId,
        handlerId,
        recipientId,
        fr_permission,
        to_permission,
        rcp_permission,
        deletedAt,
    ):
        newRequest = Request.insertNewRequest(
            type,
            content,
            createdAt,
            status,
            isDeleted,
            isWorkspaceDeleted,
            workspaceId,
            senderId,
            handlerId,
            recipientId,
            fr_permission,
            to_permission,
            rcp_permission,
            deletedAt,
        )
        return newRequest

    def deleteRequests(cls, workspaceId, requestIdList, deletedAt):
        deletedRequests = Request.deleteRequests(workspaceId, requestIdList, deletedAt)
        return deletedRequests

    def approveRequest(cls, id):
        request = Request.approveRequest(id)
        return request

    def declineRequest(cls, id):
        request = Request.declineRequest(id)
        return request
