import os
import shutil
from data.repositories.process import Process
from data.repositories.work_on import WorkOn
from services.process_service.process_version import ProcessVersionService


class ProcessService:
    @classmethod
    def create(cls, user_id, project_id, name):
        if not WorkOn.can_edit(user_id, project_id):
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
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        Process.delete(project_id, process_id)
        shutil.rmtree(f"static/{project_id}/{process_id}")

    @classmethod
    def update_name(cls, user_id, project_id, process_id, name):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        return Process.update_name(project_id, process_id, name)

    @classmethod
    def get_by_project(cls, user_id, project_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        return Process.get_by_project(project_id)
