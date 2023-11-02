from models.join_workspace import Join_Workspace
from models.recent_opened_workspaces import Recent_Opened_Workspaces


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
    def deleteMemberFromWorkspace(cls, workspaceId: str, memberId: str):
        Join_Workspace.deleteMembersFromWorkspace(workspaceId, memberId)

    @classmethod
    def updateMemberPermissions(cls, workspaceId: str, memberId: str, permission: str):
        Join_Workspace.updatePermission(workspaceId, memberId, permission)

    @classmethod
    def insertNewMember(
        cls, memberId: str, workspaceId: str, joinedAt: str, permission: str
    ):
        # check if member already joined
        member = Join_Workspace.getMember(workspaceId, memberId)
        if member is None:
            newMember = Join_Workspace.insertNewMember(
                memberId, workspaceId, joinedAt, permission
            )
            newRecentOpenedWorkspace = Recent_Opened_Workspaces.insert(
                workspaceId, memberId, joinedAt
            )
            return newMember
        return None
