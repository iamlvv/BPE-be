import os
import uuid
from fileIO.file import FileIO
from data.repositories.history_image import HistoryImage
from data.repositories.work_on import WorkOn


class ImageService:
    @classmethod
    def get_image_by_bpmn_file(self, user_id, project_id, process_id, xml_file_link):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        return HistoryImage.get_all_image_by_bpmn_file(project_id, process_id, xml_file_link)

    @classmethod
    def delete(self, user_id, project_id, process_id, xml_file_link, image_link):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        HistoryImage.delete(project_id, process_id, xml_file_link, image_link)

    @classmethod
    def insert_image(self, user_id, project_id, process_id, xml_file_link, file):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        if HistoryImage.count_all_image_by_bpmn_file(project_id, process_id, xml_file_link) == 10:
            HistoryImage.delete_oldest(project_id, process_id, xml_file_link)
        if not HistoryImage.dif_last_saved(project_id, process_id, xml_file_link):
            raise Exception("can't save 2 photos in 10s")
        rd = str(uuid.uuid1())[:8]
        extension_name = os.path.splitext(file.filename)[1]
        image_link = FileIO.save_img_file(
            file, f"{project_id}/images/{rd}{extension_name}")
        HistoryImage.insert(project_id, process_id, xml_file_link, image_link)

    @classmethod
    def bulk_insert(self, user_id, files, data):
        for file in files:
            project_id = data[file.filename]['project_id']
            process_id = data[file.filename]['process_id']
            version = data[file.filename]['version']
            xml_link = f"static/{project_id}/{process_id}/{version}.bpmn"
            self.insert_image(user_id, project_id, process_id, xml_link, file)
