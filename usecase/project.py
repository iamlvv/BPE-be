import os
from models.project import Project
from models.work_on import WorkOn, Role
from .bpmn_file import BPMNFileUsecase
from .document_file import DocumentFileUsecase
from fileIO.file import FileIO


class ProjectUsecase:
    @classmethod
    def create(cls, description, name, user_id):
        project = Project.create(description, name)
        os.makedirs(f"static/{project.id}")
        os.makedirs(f"static/{project.id}/images")
        BPMNFileUsecase.craete_default(project.id)
        DocumentFileUsecase.create_default(project.id)
        WorkOn.insert(user_id, project.id, Role.OWNER.value)
        return {
            'id': project.id,
            'name': project.name,
            'description': project.description
        }

    @classmethod
    def get(self, project_id, user_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception('permission denied')
        return Project.get(project_id)

    @classmethod
    def get_all(cls):
        return Project.get_all()

    @classmethod
    def update_name(self, user_id, project_id, name):
        if not WorkOn.is_project_owner(user_id, project_id):
            raise Exception('permisstion denied')
        Project.update_name(project_id, name)

    @classmethod
    def update_description(self, user_id, project_id, description):
        if not WorkOn.is_project_owner(user_id, project_id):
            raise Exception('permisstion denied')
        Project.update_description(project_id, description)

    @classmethod
    def update_document(self, user_id, project_id, document_link, file):
        if WorkOn.can_edit(user_id, project_id):
            DocumentFileUsecase.save(document_link, file)
            return "Success"
        else:
            raise Exception('permission denied')

    @classmethod
    def get_document(self, user_id, project_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception('permisstion denied')
        return DocumentFileUsecase.get(project_id)

    @classmethod
    def get_document_content(self, user_id, project_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception('permisstion denied')
        file_link = f"static/{project_id}/readme.md"
        return FileIO.get_content(file_link)

    @classmethod
    def get_all_project_by_user_id(self, user_id):
        return WorkOn.get_all_project_by_user_id(user_id)

    @classmethod
    def get_all_user_by_project_id(self, project_id):
        users = WorkOn.get_all_user_by_project_id(project_id)
        return users

    @classmethod
    def grant_permission(self, current_id, user_id, project_id, role):
        if WorkOn.is_project_owner(current_id, project_id):
            if role == 0:
                raise Exception('new role must not be project owner')
            if type(user_id) is not list:
                raise Exception("bad request")
            if WorkOn.is_not_exists(user_id, project_id):
                WorkOn.insert_many(user_id, project_id, role)
                return "Success"
            else:
                raise Exception('member exist')
        else:
            raise Exception('permission denied')

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
            raise Exception('permission denied')

    @classmethod
    def update_permission(self, current_id, user_id, project_id, new_role):
        if WorkOn.is_project_owner(current_id, project_id):
            if type(user_id) is not list:
                raise Exception("bad request")
            if current_id in user_id:
                raise Exception("can't update project owner")
            if new_role == 0:
                raise Exception('new role must not be project owner')
            if WorkOn.is_exists(user_id, project_id):
                WorkOn.update_many_role(user_id, project_id, new_role)
                return "Success"
            else:
                raise Exception("this user isn't project's member")
        else:
            raise Exception('permission denied')