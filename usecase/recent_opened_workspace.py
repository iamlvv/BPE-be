from models.recent_opened_workspaces import Recent_Opened_Workspaces
from datetime import datetime


class RecentOpenedWorkspaceUseCase_Get:
    pass


class RecentOpenedWorkspaceUseCase_Insert:
    @classmethod
    def insert(cls, workspaceId, memberId, joinedAt, isDeleted):
        recent_opened_workspace = Recent_Opened_Workspaces.insert(
            workspaceId, memberId, joinedAt, isDeleted
        )
        return recent_opened_workspace


class RecentOpenedWorkspaceUseCase_Update:
    @classmethod
    def pinOpenedWorkspace(cls, userId: str, workspaceId: str):
        recent_opened_workspace = Recent_Opened_Workspaces.pinOpenedWorkspace(
            workspaceId, userId
        )
        return recent_opened_workspace

    @classmethod
    def openWorkspace(cls, userId: str, workspaceId: str, openedAt: datetime):
        recent_opened_workspace = Recent_Opened_Workspaces.openWorkspace(
            workspaceId, userId, openedAt
        )
        return recent_opened_workspace


class RecentOpenedWorkspaceUseCase(
    RecentOpenedWorkspaceUseCase_Get,
    RecentOpenedWorkspaceUseCase_Insert,
    RecentOpenedWorkspaceUseCase_Update,
):
    pass
