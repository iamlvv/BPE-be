import os
import shutil
import uuid
from data.repositories.process_version import ProcessVersion
from data.repositories.process import Process
from data.repositories.comment_on import CommentOn
from fileIO.file import FileIO
from services.project_service.work_on import WorkOnService


class OldestVersionOperation:
    @classmethod
    def delete_oldest_version(cls, user_id, project_id, process_id):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        ProcessVersion.delete_oldest_version(project_id, process_id)


class ProcessVersionService_Delete:
    @classmethod
    def delete_version(cls, user_id, project_id, process_id, version):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        if len(ProcessVersion.get_by_process(project_id, process_id)) == 1:
            Process.delete(project_id, process_id)
            shutil.rmtree(f"static/{project_id}/{process_id}")
            return
        xml_link = ProcessVersion.delete(project_id, process_id, version)
        FileIO.delete(xml_link)

    @classmethod
    def delete_comment(cls, user_id, project_id, process_id, xml_file_link, id):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        if not CommentOn.owner(user_id, project_id, process_id, xml_file_link, id):
            raise Exception("permission denied")
        CommentOn.delete(id)


class ProcessVersionService_Get:
    @classmethod
    def get_all(cls):
        bpmn_files = ProcessVersion.get_all()
        return bpmn_files

    @classmethod
    def get_by_version(cls, user_id, project_id, process_id, version):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        bpmn_files = ProcessVersion.get_by_version(project_id, process_id, version)[
            "xml_file_link"
        ]
        return bpmn_files

    @classmethod
    def get_content_by_version(cls, user_id, project_id, process_id, version):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        file_link = ProcessVersion.get_by_version(project_id, process_id, version)[
            "xml_file_link"
        ]
        content = FileIO.get_content(file_link)
        return content

    @classmethod
    def get_by_process(cls, user_id, project_id, process_id):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        bpmn_files = ProcessVersion.get_by_process(project_id, process_id)
        return bpmn_files

    @classmethod
    def get_comment_by_bpmn_file(cls, user_id, project_id, process_id, xml_file_link):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        return CommentOn.get_by_bpmn_file(project_id, process_id, xml_file_link)

    @classmethod
    def get_comment_by_user(cls, user_id):
        return CommentOn.get_by_user(user_id)


class ProcessVersionService_Update:
    @classmethod
    def save(cls, xml_file_link, file, user_id, project_id, process_id, version):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        FileIO.save_bpmn_file(xml_file_link, file)
        ProcessVersion.update_version(project_id, process_id, version)

    @classmethod
    def bulk_save(cls, user_id, files, data):
        for file in files:
            project_id = data[file.filename]["project_id"]
            if not WorkOnService.can_edit(user_id, project_id):
                raise Exception("permission denied")

        for file in files:
            project_id = data[file.filename]["project_id"]
            process_id = data[file.filename]["process_id"]
            version = data[file.filename]["version"]
            xml_link = f"static/{project_id}/{process_id}/{version}.bpmn"
            FileIO.save_bpmn_file(xml_link, file)
            ProcessVersion.update_version(project_id, process_id, version)

    @classmethod
    def edit_comment(cls, user_id, project_id, process_id, xml_file_link, id, content):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        if not CommentOn.owner(user_id, project_id, process_id, xml_file_link, id):
            raise Exception("permission denied")
        CommentOn.update(id, content)


class ProcessVersionService_Insert(OldestVersionOperation):
    @classmethod
    def create_default(cls, project_id, process_id):
        version = str(uuid.uuid1())[:8]
        xml_file_link = FileIO.copy_file(
            "static/diagram.bpmn", f"{project_id}/{process_id}/{version}.bpmn"
        )

        ProcessVersion.create(xml_file_link, project_id, process_id, version)

    @classmethod
    def create_new_version(cls, user_id, file, project_id, process_id):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        if len(ProcessVersion.get_by_process(project_id, process_id)) == 5:
            raise Exception("current number of versions is equal to 5")
        version = str(uuid.uuid1())[:8]
        file_name = os.path.splitext(file.filename)[0]
        extension_name = os.path.splitext(file.filename)[1]
        xml_file_link = FileIO.create_bpmn_file(
            file, f"{project_id}/{process_id}/{version}{extension_name}"
        )

        ProcessVersion.create(xml_file_link, project_id, process_id, version)

    @classmethod
    def create_new_version_permanently(
        cls, user_id, xml_file_link, project_id, process_id
    ):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        if len(ProcessVersion.get_by_process(project_id, process_id)) == 5:
            ProcessVersionService_Insert.delete_oldest_version(project_id)
        version = str(uuid.uuid1())[:8]

        ProcessVersion.create(xml_file_link, project_id, process_id, version)

    @classmethod
    def comment(cls, user_id, project_id, process_id, xml_file_link, content):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        return CommentOn.insert(user_id, project_id, process_id, xml_file_link, content)


class ProcessVersionService(
    ProcessVersionService_Get,
    ProcessVersionService_Insert,
    ProcessVersionService_Update,
    ProcessVersionService_Delete,
):
    pass
