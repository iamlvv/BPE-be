from models.join_workspace import Join_Workspace
from models.recent_opened_workspaces import Recent_Opened_Workspaces
from models.work_on import WorkOn
from models.request import Request


class JoinWorkspaceUseCase_Get:
    @classmethod
    def getAllMembers(
        cls, workspaceId: str, page: int, limit: int, keyword=None, permission=None
    ):
        members = Join_Workspace.getAllMembers(
            workspaceId, page, limit, keyword, permission
        )
        if members is None:
            return None
        return members


class JoinWorkspaceUseCase_Update:
    @classmethod
    def deleteMember(cls, workspaceId: str, memberIdList, leftAt):
        try:
            newMemberList = Join_Workspace.removeOwnerFromMemberList(
                workspaceId, memberIdList
            )
            if len(newMemberList) == 0:
                return None
            deleteJoinWorkspace = Join_Workspace.deleteMember(
                workspaceId, newMemberList, leftAt
            )
            # when member left workspace, delete all work on project of that member
            # and delete all requests of that member

            deleteWorkOnProject = WorkOn.deleteMember(newMemberList, leftAt)
            deleteRequest = Request.deleteRequestsWhenDeletingUser(
                workspaceId, newMemberList, leftAt
            )
            return deleteJoinWorkspace
        except Exception as e:
            raise Exception(e)

    @classmethod
    def updateMemberPermission(cls, workspaceId: str, memberIdList, permission: str):
        newMemberIdList = Join_Workspace.removeOwnerFromMemberList(
            workspaceId, memberIdList
        )
        if len(newMemberIdList) == 0:
            return None
        return Join_Workspace.updatePermission(
            workspaceId, newMemberIdList, None, permission
        )

    @classmethod
    def undoDeleteMember(cls, workspaceId, memberIdList):
        return Join_Workspace.undoDeleteMember(workspaceId, memberIdList)


class JoinWorkspaceUseCase_Insert:
    @classmethod
    def insertNewMember(
        cls,
        memberId: str,
        workspaceId: str,
        joinedAt: str,
        permission: str,
    ):
        # check if member already joined
        member = Join_Workspace.getMember(workspaceId, memberId)
        isDeleted = False
        if member is not None:
            isDeleted = member.isDeleted
            if isDeleted == False:
                return None
        if member is None or isDeleted:
            newMember = Join_Workspace.insertNewMember(
                memberId, workspaceId, joinedAt, permission, isDeleted
            )
            newRecentOpenedWorkspace = Recent_Opened_Workspaces.insert(
                workspaceId, memberId, joinedAt, isDeleted
            )
            return newMember
        return None


class JoinWorkspaceUseCase(
    JoinWorkspaceUseCase_Get, JoinWorkspaceUseCase_Insert, JoinWorkspaceUseCase_Update
):
    pass
