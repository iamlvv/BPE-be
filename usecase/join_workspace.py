from models.join_workspace import Join_Workspace
from models.recent_opened_workspaces import Recent_Opened_Workspaces
from models.work_on import WorkOn


class JoinWorkspaceUseCase:
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
            deleteWorkOnProject = WorkOn.deleteMember(newMemberList, leftAt)
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
        return Join_Workspace.updatePermission(workspaceId, newMemberIdList, permission)

    @classmethod
    def insertNewMember(
        cls, memberId: str, workspaceId: str, joinedAt: str, permission: str
    ):
        # check if member already joined
        member = Join_Workspace.getMember(workspaceId, memberId)
        isDeleted = member.isDeleted
        if member is None or isDeleted:
            newMember = Join_Workspace.insertNewMember(
                memberId, workspaceId, joinedAt, permission, isDeleted
            )
            newRecentOpenedWorkspace = Recent_Opened_Workspaces.insert(
                workspaceId, memberId, joinedAt, isDeleted
            )
            return newMember
        return None

    @classmethod
    def undoDeleteMember(cls, workspaceId, memberIdList):
        return Join_Workspace.undoDeleteMember(workspaceId, memberIdList)
