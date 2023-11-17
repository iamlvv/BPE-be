from models.request import Request
from models.join_workspace import Join_Workspace
from models.notification import Notification
from models.contentNoti import generateContent
from datetime import date, datetime


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
            print("approvedRequests", approvedRequests)
            if len(approvedRequests) == 0:
                raise Exception("No request is approved")
            else:
                # if requestType is invitation, then add user to workspace
                # if requestType is adjust permission, then adjust permission
                for approvedRequest in approvedRequests:
                    print("approvedRequest", approvedRequest)
                    requestType = approvedRequest[1]
                    createdAt = datetime.now()
                    if requestType == "invitation":
                        RequestUseCase.invitation(approvedRequest, createdAt)
                    elif requestType == "adjust permission":
                        RequestUseCase.adjust_permission(approvedRequest, createdAt)
            return "Requests approved successfully"
        except Exception as e:
            raise Exception(e)

    @classmethod
    def adjust_permission(cls, approvedRequest, createdAt):
        # TODO: update permission of user in workspace
        try:
            requestType = approvedRequest[1]
            fr_permission = approvedRequest[9]
            to_permission = approvedRequest[10]
            userId = approvedRequest[8]
            workspaceId = approvedRequest[5]
            newMemberIdList = [str(userId)]
            isDeleted = False
            print(fr_permission, to_permission)
            Join_Workspace.updatePermission(
                workspaceId,
                newMemberIdList,
                currentPermission=fr_permission,
                newPermission=to_permission,
            )
            content = generateContent(
                requestType, None, fr_permission, to_permission, workspaceId, userId
            )
            Notification.insertNewNotification(
                userId, content, createdAt, isDeleted, isStarred=False, isRead=False
            )
            print(content)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def invitation(cls, approvedRequest, createdAt):
        # TODO: send notification to user
        try:
            requestType = approvedRequest[1]
            senderId = approvedRequest[6]
            memberId = approvedRequest[8]
            workspaceId = approvedRequest[5]
            permission = approvedRequest[11]
            isDeleted = False
            content = generateContent(
                requestType, permission, None, None, workspaceId, senderId
            )
            print(content)
            Notification.insertNewNotification(
                memberId, content, createdAt, isDeleted, isStarred=False, isRead=False
            )
        except Exception as e:
            raise Exception(e)

    @classmethod
    def declineRequest(cls, workspaceId, requestIdList, handlerId):
        request = Request.declineRequest(workspaceId, requestIdList, handlerId)
        return request
