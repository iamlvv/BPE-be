from cloudinary_service.cloudinary_service import cloudinary_upload
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

    @classmethod
    def get_workspace_measurements(cls, workspace_id, user_id):
        workspace = Workspace.getWorkspace(workspace_id)
        if workspace is None:
            return None
        workspace = Workspace.get_workspace_measurements(workspace_id)
        if workspace is None:
            return None
        return {
            "targetedCycleTime": workspace.targeted_cycle_time
            if workspace.targeted_cycle_time is not None
            else 0,
            "worstCycleTime": workspace.worst_cycle_time,
            "targetedCost": workspace.targeted_cost
            if workspace.targeted_cost is not None
            else 0,
            "worstCost": workspace.worst_cost,
            "targetedQuality": workspace.targeted_quality
            if workspace.targeted_quality is not None
            else 100,
            "worstQuality": workspace.worst_quality
            if workspace.worst_quality is not None
            else 0,
            "targetedFlexibility": workspace.targeted_flexibility
            if workspace.targeted_flexibility is not None
            else 100,
            "worstFlexibility": workspace.worst_flexibility
            if workspace.worst_flexibility is not None
            else 0,
            "workspaceId": int(workspace_id),
        }


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
    def updateWorkspaceBackground(cls, workspaceId, file):
        upload_result_url = cloudinary_upload(file)
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace = Workspace.updateWorkspaceBackground(
            workspaceId, background=upload_result_url
        )
        return workspace

    @classmethod
    def updateWorkspaceIcon(cls, workspaceId, file):
        upload_result_url = cloudinary_upload(file)
        workspace = Workspace.getWorkspace(workspaceId)
        if workspace is None:
            return None
        workspace = Workspace.updateWorkspaceIcon(workspaceId, upload_result_url)
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

    @classmethod
    def edit_workspace_measurements(
        cls,
        workspace_id,
        user_id,
        targeted_cycle_time,
        worst_cycle_time,
        targeted_cost,
        worst_cost,
        targeted_quality,
        worst_quality,
        targeted_flexibility,
        worst_flexibility,
    ):
        workspace = Workspace.getWorkspace(workspace_id)
        if workspace is None:
            return None
        workspace = Workspace.edit_workspace_measurements(
            workspace_id,
            targeted_cycle_time,
            worst_cycle_time,
            targeted_cost,
            worst_cost,
            targeted_quality,
            worst_quality,
            targeted_flexibility,
            worst_flexibility,
        )
        return {
            "targetedCycleTime": workspace.targeted_cycle_time
            if workspace.targeted_cycle_time
            else 0,
            "worstCycleTime": workspace.worst_cycle_time,
            "targetedCost": workspace.targeted_cost
            if workspace.targeted_cost is not None
            else 0,
            "worstCost": workspace.worst_cost,
            "targetedQuality": workspace.targeted_quality
            if workspace.targeted_quality is not None
            else 100,
            "worstQuality": workspace.worst_quality if workspace.worst_quality else 0,
            "targetedFlexibility": workspace.targeted_flexibility
            if workspace.targeted_flexibility is not None
            else 100,
            "worstFlexibility": workspace.worst_flexibility
            if workspace.worst_flexibility
            else 0,
            "workspaceId": workspace_id,
        }


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
