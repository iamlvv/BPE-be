from django.core.files.storage import FileSystemStorage
import os


class FileIO:
    @classmethod
    def save_bpmn_file(self, xml_file_link, file):
        if os.path.splitext(file.name)[1] != ".bpmn":
            raise Exception('File format is not supported')
        if file.size > 10*1024*1024:
            raise Exception('File size is larger than 10MB are not allowed')
        fs = FileSystemStorage()
        self.delete_bpmn_file(xml_file_link)
        fs.save(name=xml_file_link, content=file)

    @classmethod
    def create_bpmn_file(self, file, file_name):
        if os.path.splitext(file.name)[1] != ".bpmn":
            raise Exception('File format is not supported')
        if file.size > 10*1024*1024:
            raise Exception('File size is larger than 10MB are not allowed')
        fs = FileSystemStorage()
        file_path = 'static/bpmnfile/' + file_name
        fs.save(file_path, file)
        return file_path

    @classmethod
    def delete_bpmn_file(self, link):
        fs = FileSystemStorage()
        fs.delete(link)

    @classmethod
    def save_img_file(self, file, file_name):
        if os.path.splitext(file.name)[1] not in [".jpg", ".png", ".jpeg", ".gif"]:
            raise Exception('Image file format is not supported')
        if file.size > 10*1024*1024:
            raise Exception('File size is larger than 10MB are not allowed')
        fs = FileSystemStorage()
        file_path = 'static/image/' + file_name
        fs.save(file_path, file)
        return file_path
