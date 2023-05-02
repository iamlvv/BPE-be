from .utils import *


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.TextField()
    name = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project"

    @classmethod
    def create(cls, document, name):
        project = cls(document=document, name=name,
                      is_delete=False, create_at=datetime.now())
        project.save()
        return project

    @classmethod
    def get(self, project_id):
        project = self.objects.get(project_id=project_id)
        return {
            'name': project.name,
            'document': project.document,
            'create_at': project.create_at
        }

    @classmethod
    def get_all(cls):
        data = list(Project.objects.values())
        return data

    @classmethod
    def get_document(self, project_id):
        return self.objects.get(id=project_id).document

    @classmethod
    def update_document(self, project_id, document):
        self.objects.filter(id=project_id).update(document=document)

    @classmethod
    def get_all_project_by_project_ids(self, project_ids):
        projects = self.objects.filter(
            id__in=project_ids)
        return list(projects.values('name', 'document', 'create_at'))
