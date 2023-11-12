from models.request import Request
from models.join_workspace import Join_Workspace


class RequestUseCase:
    @classmethod
    def getAllRequests(
        cls, workspaceId, page, limit, keyword=None, type=None, status=None
    ):
        requestsList = Request.getAllRequests(
            workspaceId, page, limit, keyword, type, status
        )
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
    def createNewMemberIdList(cls, requestList):
        newMemberIdList = []
        for request in requestList:
            newMemberIdList.append(str(request["recipientId"]))
        return newMemberIdList

    @classmethod
    def approveRequest(cls, workspaceId, requestIdList, handlerId):
        try:
            approvedRequests = Request.approveRequest(
                workspaceId, requestIdList, handlerId
            )
            if len(approvedRequests) == 0:
                raise Exception("No request is approved")
            else:
                # if requestType is invitation, then add user to workspace
                # if requestType is adjust permission, then adjust permission
                for approvedRequest in approvedRequests:
                    requestType = approvedRequest[1]
                    if requestType == "invitation":
                        RequestUseCase.invitation(approvedRequest)
                    elif requestType == "adjust permission":
                        RequestUseCase.adjust_permission(approvedRequest)
            return "Requests approved successfully"
        except Exception as e:
            raise Exception(e)

    @classmethod
    def adjust_permission(cls, approvedRequest):
        # TODO: update permission of user in workspace
        try:
            to_permission = approvedRequest[10]
            userId = approvedRequest[8]
            workspaceId = approvedRequest[5]
            newMemberIdList = [str(userId)]
            Join_Workspace.updatePermission(
                workspaceId, newMemberIdList, permission=to_permission
            )
        except Exception as e:
            raise Exception(e)

    @classmethod
    def invitation(cls, approvedRequest):
        # TODO: send notification to user
        try:
            memberId = approvedRequest[8]
            workspaceId = approvedRequest[5]
            joinedAt = approvedRequest[3]
            permission = approvedRequest[11]
            isDeleted = False
            Join_Workspace.insertNewMember(
                memberId, workspaceId, joinedAt, permission, isDeleted
            )
        except Exception as e:
            raise Exception(e)

    @classmethod
    def declineRequest(cls, workspaceId, requestIdList, handlerId):
        request = Request.declineRequest(workspaceId, requestIdList, handlerId)
        return request
