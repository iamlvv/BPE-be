from datetime import datetime


class WorkspaceModel:
    id: int
    name: str
    description: str
    created_at: datetime
    ownerId: str
    background: str
    icon: str
    isPersonal: bool
    isDeleted: bool
    deletedAt: datetime


class JoinWorkspaceModel:
    workspaceId: str
    memberId: str
    permission: str
    joinedAt: datetime
    leftAt: datetime
    isDeleted: bool
    deletedAt: datetime
    isWorkspaceDeleted: bool


class RecentOpenedWorkspaceModel:
    workspaceId: int
    userId: int
    openedAt: datetime
    isHided: bool
    isPinned: bool
    isWorkspaceDeleted: bool
