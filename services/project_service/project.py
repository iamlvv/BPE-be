import os
from data.repositories.project import Project
from data.repositories.work_on import WorkOn, Role
from services.process_service.process import ProcessService
from services.file_service.document_file import DocumentFileService
from fileIO.file import FileIO


class ProjectService_Get:
    @classmethod
    def get(self, project_id, user_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        return Project.get(project_id)

    @classmethod
    def get_all(cls):
        return Project.get_all()

    @classmethod
    def get_document(self, user_id, project_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permisstion denied")
        return DocumentFileService.get(project_id)

    @classmethod
    def get_document_content(self, user_id, project_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permisstion denied")
        file_link = f"static/{project_id}/readme.md"
        return FileIO.get_content(file_link)

    @classmethod
    def get_all_project_by_user_id(
        self,
        user_id,
        page,
        limit,
        workspaceId,
        createdAt=None,
        ownerId=None,
        keyword=None,
    ):
        return WorkOn.get_all_project_by_user_id(
            user_id, page, limit, workspaceId, createdAt, ownerId, keyword
        )

    @classmethod
    def get_all_owned_project_by_user_id(self, user_id):
        return WorkOn.get_all_owned_project_by_user_id(user_id)

    @classmethod
    def get_all_shared_project_by_user_id(self, user_id):
        return WorkOn.get_all_shared_project_by_user_id(user_id)

    @classmethod
    def get_all_user_by_project_id(self, user_id, project_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        users = WorkOn.get_all_user_by_project_id(project_id)
        return users

    @classmethod
    def validate_members(self, users):
        for user in users:
            if "user_id" not in user or "role" not in user:
                raise Exception("bad request")
            if type(user["user_id"]) != int:
                raise Exception("type of user_id must be integer")
            role = user["role"]
            if role == 0:
                raise Exception("new role must not be project owner")
            if role not in [
                Role.CAN_EDIT.value,
                Role.CAN_SHARE.value,
                Role.CAN_VIEW.value,
            ]:
                raise Exception("bad request")


class ProjectService_Update:
    @classmethod
    def update_name(self, user_id, project_id, name):
        if not WorkOn.is_project_owner(user_id, project_id):
            raise Exception("permisstion denied")
        Project.update_name(project_id, name)

    @classmethod
    def update_description(self, user_id, project_id, description):
        if not WorkOn.is_project_owner(user_id, project_id):
            raise Exception("permisstion denied")
        Project.update_description(project_id, description)

    @classmethod
    def update_document(self, user_id, project_id, document_link, file):
        if WorkOn.can_edit(user_id, project_id):
            DocumentFileService.save(document_link, file)
            return "Success"
        else:
            raise Exception("permission denied")

    @classmethod
    def grant_permission(self, current_id, project_id, users):
        self.validate_members(users)
        user_ids = [user["user_id"] for user in users]
        if WorkOn.is_project_owner(current_id, project_id):
            if WorkOn.is_not_exists(user_ids, project_id):
                WorkOn.insert_many(users, project_id)
                return "Success"
            else:
                raise Exception("member exist")
        else:
            raise Exception("permission denied")

    @classmethod
    def revoke_permission(self, current_id, user_id, project_id):
        if WorkOn.is_project_owner(current_id, project_id):
            if type(user_id) is not list:
                raise Exception("bad request")
            if current_id in user_id:
                raise Exception("can't revoke project owner")
            if WorkOn.is_exists(user_id, project_id):
                WorkOn.delete_many(user_id, project_id)
                return "Success"
            else:
                raise Exception("this user isn't project's member")
        else:
            raise Exception("permission denied")

    @classmethod
    def update_permission(self, current_id, project_id, users):
        self.validate_members(users)
        user_ids = [user["user_id"] for user in users]
        if WorkOn.is_project_owner(current_id, project_id):
            if WorkOn.is_exists(user_ids, project_id):
                WorkOn.update_many_role(users, project_id)
                return "Success"
            else:
                raise Exception("this user isn't project's member")
        else:
            raise Exception("permission denied")


class ProjectService_Delete:
    @classmethod
    def delete(self, project_id, user_id):
        if not WorkOn.is_project_owner(user_id, project_id):
            raise Exception("permission denied")
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
        ProcessService.create_default(project.id, name)
        DocumentFileService.create_default(project.id)
        WorkOn.insert(user_id, project.id, Role.OWNER.value)
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
