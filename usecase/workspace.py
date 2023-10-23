import os
from models.workspace import Workspace
from models.join_workspace import Join_Workspace
from models.recent_opened_workspaces import Recent_Opened_Workspaces
from datetime import datetime


class WorkspaceUseCase:
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
        newRecentOpenedWorkspace = Recent_Opened_Workspaces.insert(
            newWorkspace.id, ownerId, createdAt
        )
        return newWorkspace

    @classmethod
    def deleteWorkspace(cls, workspaceId: str, deletedAt: str):
        if Workspace.deleteWorkspace(workspaceId, deletedAt):
            return True
        return False

    @classmethod
    def getWorkspace(cls, workspaceId: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        return workspace

    @classmethod
    def checkWorkspaceOwner(cls, workspaceId: str, ownerId: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        if workspace.ownerId == ownerId:
            return True
        return False

    @classmethod
    def updateWorkspaceName(cls, workspaceId: str, name: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace.updateWorkspaceName(workspaceId, name)
        return workspace

    @classmethod
    def updateWorkspaceDescription(cls, workspaceId: str, description: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace.updateWorkspaceDescription(workspaceId, description)
        return workspace

    @classmethod
    def changeOwnership(cls, workspaceId: str, newOwnerId: str):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace.updateWorkspaceOwnership(workspaceId, newOwnerId)
        return workspace

    @classmethod
    def updateWorkspaceBackground(cls, workspaceId, newBackground):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace.updateWorkspaceBackground(workspaceId, newBackground)
        return workspace

    @classmethod
    def updateWorkspaceIcon(cls, workspaceId, newIcon):
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace.updateWorkspaceIcon(workspaceId, newIcon)
        return workspace

    @classmethod
    def getWorkspaceByOwnerId(cls, ownerId: str):
        workspace = Workspace.getWorkspaceByOwnerId(ownerId)
        if workspace is None:
            return None
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
    def getPinnedWorkspace(cls, ownerId: str):
        workspace = Workspace.getPinnedWorkspace(ownerId)
        if workspace is None:
            return None
        return workspace

    @classmethod
    def searchWorkspaceByKeyword(cls, keyword: str):
        workspace = Workspace.searchWorkspaceByKeyword(keyword)
        if workspace is None:
            return None
        return workspace
