import os
from data.repositories.project import Project
from services.process_service.process import ProcessService
from services.file_service.document_file import DocumentFileService
from fileIO.file import FileIO
from services.project_service.work_on import WorkOnService
from data.repositories.constant import Role
from services.utils import PermissionConverter
from services.workspace_service.join_workspace import JoinWorkspaceService


class Validate:
    @classmethod
    def validate_members(cls, users):
        for user in users:
            if "user_id" not in user or "role" not in user:
                raise Exception("bad request")
            if not isinstance(user["user_id"], int):
                raise Exception("type of user_id must be integer")
            role = user["role"]
            if role == 0:
                raise Exception("new role must not be project owner")
            if role not in [
                Role.CAN_EDIT.value,
                Role.CAN_SHARE.value,
                Role.CAN_VIEW.value,
                Role.OWNER.value,
            ]:
                raise Exception("bad request")


class ProjectService_Get:
    @classmethod
    def get(cls, project_id, user_id):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        return Project.get(project_id)

    @classmethod
    def get_all(cls):
        return Project.get_all()

    @classmethod
    def get_document(cls, user_id, project_id):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        return DocumentFileService.get(project_id)

    @classmethod
    def get_document_content(cls, user_id, project_id):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        file_link = f"static/{project_id}/readme.md"
        return FileIO.get_content(file_link)

    @classmethod
    def get_all_project_by_user_id(
        cls,
        user_id,
        page,
        limit,
        workspaceId,
        createdAt=None,
        ownerId=None,
        keyword=None,
    ):
        return WorkOnService.get_all_project_by_user_id(
            user_id, page, limit, workspaceId, createdAt, ownerId, keyword
        )

    @classmethod
    def get_all_owned_project_by_user_id(cls, user_id):
        return WorkOnService.get_all_owned_project_by_user_id(user_id)

    @classmethod
    def get_all_shared_project_by_user_id(cls, user_id):
        return WorkOnService.get_all_shared_project_by_user_id(user_id)

    @classmethod
    def get_all_user_by_project_id(cls, user_id, project_id):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        users = WorkOnService.get_all_user_by_project_id(project_id)
        return users

    @classmethod
    def getAllProjectsInWorkspace(cls, workspaceId):
        return Project.getAllProjectsInWorkspace(workspaceId)


class ProjectService_Update(Validate):
    @classmethod
    def update_name(cls, user_id, project_id, name):
        if not WorkOnService.is_project_owner(user_id, project_id):
            raise Exception("permission denied")
        Project.update_name(project_id, name)

    @classmethod
    def update_description(cls, user_id, project_id, description):
        if not WorkOnService.is_project_owner(user_id, project_id):
            raise Exception("permission denied")
        Project.update_description(project_id, description)

    @classmethod
    def update_document(cls, user_id, project_id, document_link, file):
        if WorkOnService.can_edit(user_id, project_id):
            DocumentFileService.save(document_link, file)
            return "Success"
        else:
            raise Exception("permission denied")

    @classmethod
    def grant_permission(cls, current_id, project_id, users):
        ProjectService_Update.validate_members(users)
        user_ids = [user["user_id"] for user in users]
        if WorkOnService.is_project_owner(current_id, project_id):
            if WorkOnService.is_not_exists(user_ids, project_id):
                WorkOnService.insert_many(users, project_id)
                return "Success"
            else:
                # compare_permission = PermissionConverter.compare_permission(
                #     project_role, workspace_permission
                # )
                # if compare_permission:
                #     WorkOnService.update_many_role(users, project_id)
                #     return "Success"
                # else:
                #     raise Exception(
                #         "role in project must be higher or equal to permission in workspace"
                #     )
                raise Exception("permission denied")
        else:
            raise Exception("permission denied")

    @classmethod
    def revoke_permission(cls, current_id, user_id, project_id):
        if WorkOnService.is_project_owner(current_id, project_id):
            if type(user_id) is not list:
                raise Exception("bad request")
            if current_id in user_id:
                raise Exception("can't revoke project owner")
            if WorkOnService.is_exists(user_id, project_id):
                WorkOnService.delete_many(user_id, project_id)
                return "Success"
            else:
                raise Exception("this user isn't project's member")
        else:
            raise Exception("permission denied")

    @classmethod
    def update_permission(cls, current_id, project_id, users):
        ProjectService_Update.validate_members(users)
        user_ids = [user["user_id"] for user in users]
        if WorkOnService.is_project_owner(current_id, project_id):
            if WorkOnService.is_exists(user_ids, project_id):
                WorkOnService.update_many_role(users, project_id)
                return "Success"
            else:
                raise Exception("this user isn't project's member")
        else:
            raise Exception("permission denied")


class ProjectService_Delete:
    @classmethod
    def delete(cls, project_id, user_id):
        if not WorkOnService.is_project_owner(user_id, project_id):
            raise Exception("permission denied")
        # delete all work on project
        WorkOnService.delete_all(project_id)
        return Project.delete(project_id)


class ProjectService_Insert:
    @classmethod
    def create(cls, description, name, user_id, createdAt, workspaceId):
        # check if project name is already exist with this user in this workspace

        project = Project.create(description, name, user_id, createdAt, workspaceId)
        if not os.path.isdir(f"static/{project.id}"):
            os.makedirs(f"static/{project.id}")
            if not os.path.isdir(f"static/{project.id}/images"):
                os.makedirs(f"static/{project.id}/images")

        # get list of member id in workspace and permission
        list_members_id_and_permission = (
            JoinWorkspaceService.getListMemberIdAndPermissionInWorkspace(workspaceId)
        )
        print("list_members_id_and_permission", list_members_id_and_permission)
        # convert permission to role
        list_members_id_and_permission = [
            {
                "user_id": member[0],
                "role": PermissionConverter.convert_permission_to_role(member[1]),
            }
            for member in list_members_id_and_permission
        ]
        print("this is new list", list_members_id_and_permission)
        ProcessService.create_default(project.id, name)
        DocumentFileService.create_default(project.id)
        # WorkOnService.insert(user_id, project.id, Role.OWNER.value)
        # insert all member in workspace to work on project with default role is their permission in workspace
        WorkOnService.insert_many(list_members_id_and_permission, project.id)
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "createdAt": project.create_at,
            "ownerId": project.ownerId,
            "workspaceId": project.workspaceId,
        }


class ProjectService(
    ProjectService_Get,
    ProjectService_Delete,
    ProjectService_Insert,
    ProjectService_Update,
):
    pass
