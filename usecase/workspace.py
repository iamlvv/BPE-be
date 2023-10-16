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
        return newWorkspace

    @classmethod
    def deleteWorkspace(cls, workspaceId: str):
        if Workspace.deleteWorkspace(workspaceId):
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
