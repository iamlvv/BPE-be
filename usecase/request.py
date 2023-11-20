from models.request import Request
from models.join_workspace import Join_Workspace
from models.notification import Notification
from models.contentNoti import generateContent
from datetime import date, datetime


class NewMemberIdList:
    @classmethod
    def createNewMemberIdList(cls, requestList):
        newMemberIdList = []
        for request in requestList:
            newMemberIdList.append(str(request["recipientId"]))
        return newMemberIdList


class RequestUseCase_Get(NewMemberIdList):
    @classmethod
    def getAllRequests(
        cls, workspaceId, page, limit, keyword=None, type=None, status=None
    ):
        requestsList = Request.getAllRequests(
            workspaceId, page, limit, keyword, type, status
        )
        return requestsList


class RequestUseCase_Update(NewMemberIdList):
    @classmethod
    def deleteRequests(cls, workspaceId, requestIdList, deletedAt):
        deletedRequests = Request.deleteRequests(workspaceId, requestIdList, deletedAt)
        return deletedRequests

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
                    requestType = approvedRequest["type"]
                    createdAt = datetime.now()
                    if requestType == "invitation":
                        RequestUseCase.invitation(approvedRequest, createdAt)
                    elif requestType == "adjust permission":
                        RequestUseCase.adjust_permission(approvedRequest, createdAt)
            return approvedRequests
        except Exception as e:
            raise Exception(e)

    @classmethod
    def adjust_permission(cls, approvedRequest, createdAt):
        # TODO: update permission of user in workspace
        try:
            requestType = approvedRequest["type"]
            fr_permission = approvedRequest["frPermission"]
            to_permission = approvedRequest["toPermission"]
            userId = approvedRequest["recipientId"]
            workspaceId = approvedRequest["workspaceId"]
            newMemberIdList = [str(userId)]
            isDeleted = False
            notificationType = "adjust permission"
            status = "approved"
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
                userId,
                content,
                createdAt,
                isDeleted,
                isStarred=False,
                isRead=False,
                notificationType=notificationType,
                status=status,
                workspaceId=workspaceId,
                permission=to_permission,
            )
            print(content)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def invitation(cls, approvedRequest, createdAt):
        # TODO: send notification to user
        try:
            requestType = approvedRequest["type"]
            senderId = approvedRequest["senderId"]
            memberId = approvedRequest["recipientId"]
            workspaceId = approvedRequest["workspaceId"]
            permission = approvedRequest["rcpPermission"]
            notificationType = "invitation"
            status = "pending"
            isDeleted = False
            content = generateContent(
                requestType, permission, None, None, workspaceId, senderId
            )
            print(content)
            Notification.insertNewNotification(
                memberId,
                content,
                createdAt,
                isDeleted,
                isStarred=False,
                isRead=False,
                notificationType=notificationType,
                status=status,
                workspaceId=workspaceId,
                permission=permission,
            )
        except Exception as e:
            raise Exception(e)

    @classmethod
    def declineRequest(cls, workspaceId, requestIdList, handlerId):
        request = Request.declineRequest(workspaceId, requestIdList, handlerId)
        return request


class RequestUseCase_Insert(NewMemberIdList):
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
        # check the permission of sender Id
        # if sender is viewer, then rcp_permission must be viewer
        # if sender is sharer, then rcp_permission must be viewer or sharer
        # if sender is editor, then rcp_permission must be viewer, sharer or editor
        # if sender is owner, then rcp_permission can be any permission

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


class RequestUseCase(RequestUseCase_Get, RequestUseCase_Insert, RequestUseCase_Update):
    pass
