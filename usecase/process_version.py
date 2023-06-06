import os
import shutil
import uuid
from models.process_version import ProcessVersion
from models.process import Process
from models.work_on import WorkOn
from models.comment_on import CommentOn
from fileIO.file import FileIO


class ProcessVersionUsecase:
    @classmethod
    def save(self, xml_file_link, file, user_id, project_id, process_id, version):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        FileIO.save_bpmn_file(xml_file_link, file)
        ProcessVersion.update_version(project_id, process_id, version)

    @classmethod
    def create_default(self, project_id, process_id):
        version = str(uuid.uuid1())[:8]
        xml_file_link = FileIO.copy_file(
            "static/diagram.bpmn", f"{project_id}/{process_id}/{version}.bpmn")

        ProcessVersion.create(xml_file_link, project_id, process_id, version)

    @classmethod
    def create_new_version(self, user_id, file, project_id, process_id):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        if len(ProcessVersion.get_by_process(project_id, process_id)) == 5:
            raise Exception("current number of versions is equal to 5")
        version = str(uuid.uuid1())[:8]
        file_name = os.path.splitext(file.filename)[0]
        extension_name = os.path.splitext(file.filename)[1]
        xml_file_link = FileIO.create_bpmn_file(
            file, f"{project_id}/{process_id}/{version}{extension_name}")

        ProcessVersion.create(xml_file_link, project_id, process_id, version)

    @classmethod
    def create_new_version_permanently(self, user_id, xml_file_link, project_id, process_id):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        if len(ProcessVersion.get_by_process(project_id, process_id)) == 5:
            self.delete_oldest_version(project_id)
        version = str(uuid.uuid1())[:8]

        ProcessVersion.create(xml_file_link, project_id, process_id, version)

    @classmethod
    def get_all(self):
        bpmn_files = ProcessVersion.get_all()
        return bpmn_files

    @classmethod
    def get_by_version(self, user_id, project_id, process_id, version):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        bpmn_files = ProcessVersion.get_by_version(
            project_id, process_id, version)['xml_file_link']
        return bpmn_files

    @classmethod
    def get_content_by_version(self, user_id, project_id, process_id, version):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        file_link = ProcessVersion.get_by_version(
            project_id, process_id, version)['xml_file_link']
        content = FileIO.get_content(file_link)
        return content

    @classmethod
    def get_by_process(self, user_id, project_id, process_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        bpmn_files = ProcessVersion.get_by_process(project_id, process_id)
        return bpmn_files

    @classmethod
    def delete_version(self, user_id, project_id, process_id, version):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        if len(ProcessVersion.get_by_process(project_id, process_id)) == 1:
            Process.delete(project_id, process_id)
            shutil.rmtree(f'static/{project_id}/{process_id}')
            return
        xml_link = ProcessVersion.delete(project_id, process_id, version)
        FileIO.delete(xml_link)

    @classmethod
    def delete_oldest_version(self, user_id, project_id, process_id):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        ProcessVersion.delete_oldest_version(project_id, process_id)

    @classmethod
    def comment(self, user_id, project_id, process_id, xml_file_link, content):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        return CommentOn.insert(user_id, project_id, process_id, xml_file_link, content)

    @classmethod
    def edit_comment(self, user_id, project_id, process_id, xml_file_link, id, content):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        if not CommentOn.owner(user_id, project_id, process_id, xml_file_link, id):
            raise Exception("permission denied")
        CommentOn.update(id, content)

    @classmethod
    def delete_comment(self, user_id, project_id, process_id, xml_file_link, id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        if not CommentOn.owner(user_id, project_id, process_id, xml_file_link, id):
            raise Exception("permission denied")
        CommentOn.delete(id)

    @classmethod
    def get_comment_by_bpmn_file(self, user_id, project_id, process_id, xml_file_link):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        return CommentOn.get_by_bpmn_file(project_id, process_id, xml_file_link)

    @classmethod
    def get_comment_by_user(self, user_id):
        return CommentOn.get_by_user(user_id)
