from django.core.files.storage import FileSystemStorage


class FileIO:
    @classmethod
    def save(self, xml_file_link, file):
        fs = FileSystemStorage()
        self.delete(xml_file_link)
        fs.save(name=xml_file_link, content=file)

    @classmethod
    def create(self, file, file_name):
        fs = FileSystemStorage()
        file_path = 'static/' + file_name
        fs.save(file_path, file)
        return file_path

    @classmethod
    def delete(self, xml_file_link):
        fs = FileSystemStorage()
        fs.delete(xml_file_link)
