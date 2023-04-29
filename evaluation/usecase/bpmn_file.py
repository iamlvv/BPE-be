import uuid
from datetime import datetime
from evaluation.models.bpmn_file import BPMNFile
from evaluation.models.work_on import WorkOn, Role
from evaluation.fileIO.file import FileIO


class BPMNFileUsecase:
    @classmethod
    def save(self, xml_file_link, file, user_id, project_id, version):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permisstion denied")
        FileIO.save(xml_file_link, file)
        BPMNFile.update_version(project_id, version)

    @classmethod
    def create_new_version(self, user_id, file, project_id):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permisstion denied")
        if len(BPMNFile.get_by_project(project_id)) == 5:
            raise Exception("current number of versions is equal to 5")
        version = str(uuid.uuid1())[:8]
        xml_file_link = FileIO.create(file, version + '_' + file.name)

        BPMNFile.create(xml_file_link, project_id, version)

    @classmethod
    def create_new_version_permanently(self, user_id, xml_file_link, project_id):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permisstion denied")
        if len(BPMNFile.get_by_project(project_id)) == 5:
            self.delete_oldest_version(project_id)
        version = str(uuid.uuid1())[:8]

        BPMNFile.create(xml_file_link, project_id,
                        version, datetime.now())

    @classmethod
    def get_all(self):
        bpmn_files = BPMNFile.get_all()
        return bpmn_files

    @classmethod
    def get_by_version(self, user_id, project_id, version):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permisstion denied")
        bpmn_files = BPMNFile.get_by_version(project_id, version)
        if len(bpmn_files) == 0:
            raise Exception("version doesn't exist")
        return bpmn_files[0]

    @classmethod
    def get_by_project(self, user_id, project_id):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permisstion denied")
        bpmn_files = BPMNFile.get_by_project(project_id)
        return bpmn_files

    @classmethod
    def delete_version(self, user_id, project_id, version):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permisstion denied")
        xml_link = BPMNFile.delete(project_id, version)
        FileIO.delete(xml_link)

    @classmethod
    def delete_oldest_version(self, user_id, project_id):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permisstion denied")
        BPMNFile.delete_oldest_version(project_id)
