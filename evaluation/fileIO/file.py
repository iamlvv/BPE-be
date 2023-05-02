from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import os


class FileIO:
    @classmethod
    def copy_file(self, path1, file_name):
        fs = FileSystemStorage()
        f = fs.open(path1, 'r')
        fs1 = FileSystemStorage()
        file_path = 'static/' + file_name
        fs1.save(file_path, f)
        return file_path

    @classmethod
    def save_bpmn_file(self, xml_file_link, file):
        if os.path.splitext(file.name)[1] != ".bpmn":
            raise Exception('File format is not supported')
        if file.size > 10*1024*1024:
            raise Exception('File size is larger than 10MB are not allowed')
        fs = FileSystemStorage()
        self.delete(xml_file_link)
        fs.save(name=xml_file_link, content=file)

    @classmethod
    def create_bpmn_file(self, file, file_name):
        if os.path.splitext(file.name)[1] != ".bpmn":
            raise Exception('File format is not supported')
        if file.size > 10*1024*1024:
            raise Exception('File size is larger than 10MB are not allowed')
        fs = FileSystemStorage()
        file_path = 'static/' + file_name
        fs.save(file_path, file)
        return file_path

    @classmethod
    def delete(self, link):
        fs = FileSystemStorage()
        fs.delete(link)

    @classmethod
    def save_img_file(self, file, file_name):
        if os.path.splitext(file.name)[1] not in [".jpg", ".png", ".jpeg", ".gif"]:
            raise Exception('Image file format is not supported')
        if file.size > 10*1024*1024:
            raise Exception('File size is larger than 10MB are not allowed')
        fs = FileSystemStorage()
        file_path = 'static/' + file_name
        fs.save(file_path, file)
        return file_path

    @classmethod
    def create_default_md_file(self, file_name):
        fs = FileSystemStorage()
        file_path = 'static/' + file_name
        fs.save(name=file_path, content=ContentFile(""))
        return file_path

    @classmethod
    def save_md_file(self, file_link, new_file):
        if os.path.splitext(new_file.name)[1] not in [".md"]:
            raise Exception('Markdown file format is not supported')
        if new_file.size > 10*1024*1024:
            raise Exception('File size is larger than 10MB are not allowed')
        fs = FileSystemStorage()
        self.delete(file_link)
        fs.save(name=file_link, content=new_file)
