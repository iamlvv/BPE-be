from data.repositories.workspace import Workspace
from data.repositories.recent_opened_workspaces import Recent_Opened_Workspaces
from services.workspace_service.join_workspace import JoinWorkspaceService
from datetime import datetime


class WorkspaceService_Get:
    @classmethod
    def getWorkspace(cls, workspaceId: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        return workspace

    @classmethod
    def getAllWorkspacesByUser(
        cls,
        user_id,
        page,
        limit,
        openedAt=None,
        ownerId=None,
        keyword=None,
        pinned=None,
    ):
        workspace = Workspace.getAllWorkspacesByUser(
            user_id, page, limit, openedAt, ownerId, keyword, pinned
        )
        if workspace is None:
            return None
        return workspace

    @classmethod
    def getPinnedWorkspace(cls, userId: str):
        workspace = Workspace.getPinnedWorkspace(userId)
        if workspace is None:
            return None
        return workspace

    @classmethod
    def getTotalWorkspacesByUser(cls, userId: str):
        workspace = Workspace.getTotalWorkspacesByUser(userId)
        if workspace is None:
            return None
        return workspace

    @classmethod
    def checkWorkspaceOwner(cls, workspaceId, ownerId):
        workspaceId = Workspace.getWorkspace(workspaceId)
        if workspaceId is None:
            return None
        if workspaceId == ownerId:
            return True
        return False

    @classmethod
    def searchWorkspaceByKeyword(cls, keyword: str, userId: str):
        workspace = Workspace.searchWorkspaceByKeyword(keyword, userId)
        if workspace is None:
            return None
        return workspace


class WorkspaceService_Update:
    @classmethod
    def updateWorkspaceName(cls, workspaceId: str, name: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace = Workspace.updateWorkspaceName(workspaceId, name)
        return workspace

    @classmethod
    def updateWorkspaceDescription(cls, workspaceId: str, description: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace = Workspace.updateWorkspaceDescription(workspaceId, description)
        return workspace

    @classmethod
    def changeOwnership(cls, workspaceId: str, newOwnerId: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace = Workspace.updateWorkspaceOwnership(workspaceId, newOwnerId)
        return workspace

    @classmethod
    def updateWorkspaceBackground(cls, workspaceId, newBackground):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace = Workspace.updateWorkspaceBackground(workspaceId, newBackground)
        return workspace

    @classmethod
    def updateWorkspaceIcon(cls, workspaceId, newIcon):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace = Workspace.updateWorkspaceIcon(workspaceId, newIcon)
        return workspace

    @classmethod
    def pinWorkspace(cls, userId: str, workspaceId: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        recent_opened_workspace = Recent_Opened_Workspaces.pinOpenedWorkspace(
            workspaceId, userId
        )
        return recent_opened_workspace

    @classmethod
    def openWorkspace(cls, userId: str, workspaceId: str, openedAt: datetime):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        recent_opened_workspace = Recent_Opened_Workspaces.openWorkspace(
            workspaceId, userId, openedAt
        )
        return recent_opened_workspace


class WorkspaceService_Delete:
    @classmethod
    def deleteWorkspace(cls, workspaceId: str, deletedAt: str):
        if Workspace.deleteWorkspace(workspaceId, deletedAt):
            return True
        return False


class WorkspaceService_Insert:
    @classmethod
    def createNewWorkspace(
        cls,
        name: str,
        description: str,
        createdAt: datetime,
        ownerId: str,
        background: str,
        icon: str,
        isPersonal: bool,
        isDeleted: bool,
    ):
        # check if workspace name is existed with the same owner
        workspace = Workspace.checkIfWorkspaceExists(name, ownerId)
        if workspace is not None:
            return None
        newWorkspace = Workspace.insertNewWorkspace(
            name,
            description,
            createdAt,
            ownerId,
            background,
            icon,
            isPersonal,
            isDeleted,
        )

        if newWorkspace is None:
            return None
        # newRecentOpenedWorkspace = Recent_Opened_Workspaces.insert(
        #     newWorkspace.id, ownerId, createdAt, isDeleted
        # )
        # newJoinWorkspace = Join_Workspace.insertNewMember(
        #     ownerId, newWorkspace.id, createdAt, "owner", isDeleted
        # )
        newJoinWorkspace = JoinWorkspaceService.insertNewMember(
            ownerId, newWorkspace.id, createdAt, "owner"
        )
        return newWorkspace


class WorkspaceService(
    WorkspaceService_Get,
    WorkspaceService_Insert,
    WorkspaceService_Update,
    WorkspaceService_Delete,
):
    pass
