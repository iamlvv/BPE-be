import uuid
from evaluation.models.document_file import DocumentFile
from evaluation.fileIO.file import FileIO


class DocumentFileUsecase:
    @classmethod
    def create_default(self, project_id):
        document_link = FileIO.create_default_md_file(
            f"{project_id}/readme.md")
        DocumentFile.create(document_link, project_id)

    @classmethod
    def save(self, document_link, file):
        FileIO.save_md_file(document_link, file)
        DocumentFile.update(document_link)
