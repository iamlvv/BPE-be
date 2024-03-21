import os
import shutil
from data.repositories.process import Process
from services.process_service.process_version import ProcessVersionService
from services.project_service.work_on import WorkOnService
from services.utils import Permission_check


class ProcessService:
    @classmethod
    def create(cls, user_id, project_id, name):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")

        process = Process.insert(project_id, name)
        if not os.path.isdir(f"static/{project_id}/{process.id}"):
            os.makedirs(f"static/{project_id}/{process.id}")
        ProcessVersionService.create_default(project_id, process.id)
        return process

    @classmethod
    def create_default(cls, project_id, name):
        process = Process.insert(project_id, name)
        if not os.path.isdir(f"static/{project_id}/{process.id}"):
            os.makedirs(f"static/{project_id}/{process.id}")
        ProcessVersionService.create_default(project_id, process.id)
        return process

    @classmethod
    def delete(cls, user_id, project_id, process_id):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        Process.delete(project_id, process_id)
        shutil.rmtree(f"static/{project_id}/{process_id}")

    @classmethod
    def update_name(cls, user_id, project_id, process_id, name):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        return Process.update_name(project_id, process_id, name)

    @classmethod
    def get_by_project(cls, user_id, project_id):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        return Process.get_by_project(project_id)

    @classmethod
    def get_all_active_process_versions_in_workspace(
        cls, workspace_id, project_id, user_id
    ):
        # get all projects in workspace
        # in each project, get all processes that has active process_version
        # check if user is workspace_owner
        workspace_owner = Permission_check.check_if_user_is_workspace_owner(
            workspace_id, user_id
        )
        active_process_versions_list = (
            ProcessVersionService.get_all_active_process_versions_in_workspace(
                project_id
            )
        )
        return active_process_versions_list
