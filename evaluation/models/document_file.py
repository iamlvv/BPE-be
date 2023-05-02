from .utils import *


class DocumentFile(models.Model):
    document_link = models.TextField()
    project_id = models.BigIntegerField()
    last_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document_file"
        unique_together = (('document_link', 'project_id'),)

    @classmethod
    def create(cls, document_link, project_id):
        document_file = cls(document_link=document_link,
                            project_id=project_id, last_saved=datetime.now())
        document_file.save()
        return document_file

    @classmethod
    def update(self, document_link):
        self.objects.filter(document_link=document_link).update(
            last_saved=datetime.now())

    @classmethod
    def get(self, project_id):
        obj = self.objects.filter(project_id=project_id).values(
            'project_id', 'document_link', 'last_saved')
        if len(obj) == 0:
            raise Exception('project_id incorrect')
        return list(obj)[0]
