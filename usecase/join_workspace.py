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
    def deleteMember(cls, workspaceId: str, memberIdList):
        try:
            deleteJoinWorkspace = Join_Workspace.deleteMember(workspaceId, memberIdList)
            deleteWorkOnProject = WorkOn.deleteMember(memberIdList)
            return deleteJoinWorkspace
        except Exception as e:
            raise Exception(e)

    @classmethod
    def updateMemberPermission(cls, workspaceId: str, memberIdList, permission: str):
        return Join_Workspace.updatePermission(workspaceId, memberIdList, permission)

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
